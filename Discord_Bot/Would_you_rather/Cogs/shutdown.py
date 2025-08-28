import asyncio
from discord.ext import commands

class Shutdown(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command(name="shutdown")
  @commands.is_owner()
  async def shutdown(self, ctx):
    await ctx.send("🛑 Shutting down...")
    await self.bot.close()

async def setup(bot):
  await bot.add_cog(Shutdown(bot))
