import pytest
import discord
from main import create_db_pool, bot
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_database_connection():
  pool = await create_db_pool()
  async with pool.acquire() as conn:
    result = await conn.fetch("SELECT 1")
  assert result[0]["?column?"] == 1

@pytest.mark.asyncio
async def test_discord_connection():
  bot.on_ready = AsyncMock()
  await bot.on_ready()

  bot.on_ready.assert_awaited_once()

