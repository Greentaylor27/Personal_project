import os
import random
import asyncio
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
# Initialize Supabase client
# --------------------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
  print(f"✅ Bot connected as {bot.user}")

async def load_cogs():
  for filename in os.listdir("./Cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
      await bot.load_extension(f"Cogs.{filename[:-3]}")
      print(f"Loaded Cogs: {filename}")

async def main():
  await load_cogs()
  await bot.start(DISCORD_TOKEN)


# Need to add a proper exit() for closing connection to bot so I'm not Ctrl+C to exit.


asyncio.run(main())
