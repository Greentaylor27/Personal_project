import os
import asyncio
import signal
from dotenv import load_dotenv
import discord
from discord.ext import commands
from supabase import create_client, Client



# --------------------
# Load environment variables
# --------------------
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# --------------------
# Initialize Supabase client (sync)
# --------------------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --------------------
# Async wrapper for supabase
# --------------------
async def supabase_query(query_fn, *args, **kwargs):
  """
  Runs Supabase query in the thread rather than the queue
  Example:
    response = await supabase_query(
      supabase.table("users").select("*").eq("id", 123).execute()
    )
  """
  return await asyncio.to_thread(query_fn, *args, **kwargs)


# --------------------
# Discord bot initialization
# --------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.supabase = supabase
bot.supabase_query = supabase_query

# --------------------
# Events
# --------------------
@bot.event
async def on_ready():
  print(f"✅ Bot connected as {bot.user}")


# --------------------
# Cog loader
# --------------------
async def load_cogs():
  for filename in os.listdir("./Cogs"):
    if filename.endswith(".py") and filename not in "__init__.py":
      await bot.load_extension(f"Cogs.{filename[:-3]}")
      print(f"Loaded Cog: {filename}")

# --------------------
# Graceful Shutdown handler
# --------------------
def shutdown_handler():
  """Called on SIGINT / SIGTERM (Ctrl+c or kill)"""
  loop = asyncio.get_event_loop()
  if loop.is_running():
    loop.create_task(bot.close())


# --------------------
# Main entrypoint
# --------------------
async def main():
  # Register signal handlers for Ctrl+C / termination
  loop = asyncio.get_running_loop()
  for sig in (signal.SIGINT, signal.SIGTERM):
    loop.add_signal_handler(sig, shutdown_handler)

  # Load cogs and run bot inside context manager
  async with bot:
    await load_cogs()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("🛑 Bot stopped by user")
