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

# --------------------
# Initialize Discord bot
# --------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------
# Ping command (Test)
# --------------------
@bot.command(name="ping")
async def ping(ctx):
  await ctx.send("Pong!")

bot.run(DISCORD_TOKEN)
