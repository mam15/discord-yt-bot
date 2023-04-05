# discord-yt-bot
A bot for playing Youtube audio on Discord

## Dependencies
This bot requires `discord.py`, `google-api-python-client` and `yt-dlp` as dependencies. You can install them with pip by running:
```
pip install discord.py google-api-python-client yt-dlp
```
If you want to run automated tests, you also need `pytest` and `pytest-asyncio`:
```
pip install pytest pytest-asyncio
```
## Usage
In order to use this bot, you need to add a Discord app token on the `.env` file ([here](https://discord.com/developers/docs/getting-started) is a guide on creating a Discord app), as well as a Youtube API key, so that we can query Youtube videos using text search ([here](https://developers.google.com/youtube/v3/getting-started) you can learn to generate your API key). After adding the token and API key, and adding the bot to your Discord server, all you have to do is run `python3 bot.py` and the bot will be online.

**Important: NEVER commit or share your Youtube API key or Discord token with anyone! They can be used maliciously and must be kept secret.**

You can play a Youtube video by typing `!play {video name}` on your Discord server. The "!" command prefix can be modified in the `.env` file. This is a very simple bot, so it has no other features.
