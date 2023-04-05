from discord.errors import LoginFailure
import pytest
from bot import main
import os

@pytest.mark.asyncio
async def test_main_notoken():
    with pytest.raises(LoginFailure):
        os.environ["discord_token"] = "Invalid Discord token"
        await main()
