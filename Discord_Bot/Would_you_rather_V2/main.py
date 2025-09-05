import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncpg

# --------------------
# Load environment variables
# --------------------
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# --------------------
# Async PostGres connection
# --------------------
async def create_db_pool():
  return await asyncpg.create_pool(DATABASE_URL)

# --------------------
# Discord bot setup
# --------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Placeholder for the db poll
bot.db_pool = None

# --------------------
# Events
# --------------------
@bot.event
async def on_ready():
  print(f"✅ Bot connected as {bot.user}")

@bot.event
async def on_close():
  print("🧹 Cleaning up before shutdown...")
  await bot.db_pool.close()

# --------------------
# Cog loader
# --------------------
async def load_cogs():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
      await bot.load_extension(f"cogs.{filename[:-3]}")
      print(f"Loaded Cog: {filename}")

# --------------------
# Main entry point
# --------------------
async def main():
  # connect to PostGres
  bot.db_pool = await create_db_pool()
  print("🗄️ Database connected successfully!")

  # Load Cogs
  await load_cogs()

  # Start the Bot
  await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except (KeyboardInterrupt, asyncio.CancelledError):
    print("🛑 Bot stopped by user or task cancelled.")
