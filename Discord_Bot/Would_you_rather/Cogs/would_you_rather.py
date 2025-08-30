import random
import discord
import asyncio
from discord.ext import commands
from Utils.utils_db import get_random_question, get_user, add_user
from main import supabase_query



class WouldYouRather(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.supabase = bot.supabase
    self.active_wyr = {} # key: channel_id, value: message object
    self.votes = {} # key: channel_id, value: dict of {user_id: "A" or "B"}

  async def ensure_user_registered(self, user: discord.User):
    """Check if user exists in DB, if not register them as collaborator."""
    user_id = 108101984430628864
    username = str(user)

    print(f"User id: {user_id}\nUsername: {username}")

    print(f"Response before: {response}")

    response = await get_user(self.supabase, user_id)
    if response.data:
      return response.data[0]
    
    print(f"Response after: {response}")
    
    insert_reponse = await add_user(self.supabase, user_id, username)
    return insert_reponse.data[0] if insert_reponse.data else None

  @commands.command(name="wyr")
  async def would_you_rather(self, ctx):
    """Start a Would You Rather question."""

    print("Starting up would you rather")

    # Auto Register users
    print("Running auto register")
    user_row = await self.ensure_user_registered(ctx.author)
    if not user_row:
      await ctx.send("⚠️ Failed to register user, please try again.")

    # Helper to keep track of active game running
    if ctx.channel.id in self.active_wyr:
      await ctx.send(
        "⚠️ A WYR is already running in this channel! "
        "Use `!wyr_current` to see it and vote."
      )
      return
    

    # Step 1: fetch a random question
    print("Getting random question")
    question = get_random_question(self.supabase, "questions")
    if not question:
      await ctx.send("No questions found!")
      return
    
    print("Grabbing options from question")
    option_a = question["option_a"]
    option_b = question["option_b"]
    print(f"Option A: {option_a}, Option B: {option_b}")

    # Step 2: Create an embed with the question and instructions
    print("Making embed")
    embed = discord.Embed(
      title="🤔 Would you Rather...",
      description=f"**{option_a}** ***OR*** **{option_b}**",
      color=discord.Color.blurple()
    )
    embed.add_field(name="Vote", value="React with 🅰️ for option A, 🅱️ for option B")
    embed.add_field(name="🅰️", value=option_a, inline=False)
    embed.add_field(name="🅱️", value=option_b, inline=False)
    print("Embed made")

    # Step 3: send embed and add reactions for voting
    print("Sending embed")
    message = await ctx.send(embed=embed)
    await message.add_reaction("🅰️")
    await message.add_reaction("🅱️")
    print("embed sent")

    # Storing active WYR
    self.active_wyr[ctx.channel.id] = message

    def check(reaction, user):
      return (
        user != self.bot.user
        and reaction.message.id == message.id
        and str(reaction.emoji) in ["🅰️", "🅱️"]
      )
    
    try:
      while True:
        reaction, user = await self.bot.wait_for("reaction_add", timeout=120.0, check=check)
        self.votes.setdefault(ctx.channel.id, {})[user.id] = str(reaction.emoji)
    except asyncio.TimeoutError:
      await ctx.send("⏰ Voting time ended! Results are in!!")
      votes = self.votes.get(ctx.channel.id, {})
      total_votes = len(votes)
      count_a = sum(1 for v in votes.values() if v == "🅰️")
      count_b = sum(1 for v in votes.values() if v == "🅱️")

      percent_a = round((count_a / total_votes) * 100) if total_votes else 0
      percent_b = round((count_b / total_votes) * 100) if total_votes else 0

      embed = discord.Embed(
        title="📊 WYR Poll Results",
        description=f"🅰️ **{option_a}** vs 🅱️ **{option_b}**",
        color=discord.Color.green()
      )
      embed.add_field(name="🅰️ Votes", value=f"{count_a} ({percent_a}%)", inline=True)
      embed.add_field(name="🅱️ Votes", value=f"{count_b} ({percent_b}%)", inline=True)
      embed.set_footer(text="Poll ended!")

      await ctx.send(embed=embed)

      # Deletes original message to keep servers clean
      try:
        await message.delete()
      except discord.NotFound:
        pass # Message has already been deleted

      # Cleanup
      self.active_wyr.pop(ctx.channel.id, None)
      self.votes.pop(ctx.channel.id, None)

  @commands.command(name="wyr_current")
  async def wyr_current(self, ctx):
    """Redisplay the current WYR for voting"""
    message = self.active_wyr.get(ctx.channel.id)
    if not message:
      await ctx.send("There is no active WYR in this channel.")
      return
    
    votes = self.votes.get(ctx.channel.id, {})
    total_votes = len(votes)
    count_a = sum(1 for v in votes.values() if v == "🅰️")
    count_b = sum(1 for v in votes.values() if v == "🅱️")

    embed = discord.Embed(
      title="🕒 Current WYR Poll",
      description=f"Vote on the current WYR here: [Jump to message]({message.jump_url})",
      color=discord.Color.blue()
    )
    embed.add_field(name="🅰️ Votes", value=f"{count_a}", inline=True)
    embed.add_field(name="🅱️ Votes", value=f"{count_b}", inline=True)
    embed.set_footer(text=f"Total votes: {total_votes}")

    await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
  await bot.add_cog(WouldYouRather(bot))
