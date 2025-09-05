import asyncio
import signal
import discord
from discord.ext import commands

class Shutdown(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    # Register signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
      loop.add_signal_handler(sig, lambda: asyncio.create_task(self.handle_signal()))

  async def handle_signal(self):
    """Gracefully shuts down the bot on SIGINT/SIGTERM."""
    loop = asyncio.get_event_loop()

    print(" Graceful shutdown initiated via signal...")
    for task in asyncio.all_tasks():
      if task is not asyncio.current_task():
        task.cancel()

    await self.bot.close()

  @commands.command(name="shutdown")
  @commands.is_owner() # Only the bot own can call this
  async def shutdown(self, ctx: commands.Context):
    """Manually shuts down the bot."""
    await ctx.send("🛑 Shutting down gracefully...")
    await self.bot.close()


async def setup(bot: commands.Bot):
  await bot.add_cog(Shutdown(bot))
