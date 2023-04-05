import asyncio
import os
from dotenv import load_dotenv
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import yt_dlp
import discord

class YoutubeStream:

    load_dotenv()
    service_name = "youtube"
    api_version = "v3"
    api_key = os.getenv("yt_api_key")

    ydl_options = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'nowarnings': True,
        'restrictfilenames': True,
        'source_address': '0.0.0.0',
    }
    ydl = yt_dlp.YoutubeDL(ydl_options)

    def __init__(self):
        self.youtube = googleapiclient.discovery.build(self.service_name, self.api_version, developerKey=self.api_key)

    def _search(self, query):
        s = self.youtube.search().list(
                q=query,
                part="id",
                type="video",
                maxResults=1)
        try:
            response = s.execute()
            if not response["items"]:
                raise ValueError(f"No results for query '{query}'")
            return response["items"][0]["id"]["videoId"]
        except HttpError as e:
            print(f"Youtube API error: {e.reason}")
            raise e

    async def stream(self, query, loop=None):
        loop = loop or asyncio.get_event_loop()
        videoId = await loop.run_in_executor(None, lambda:self._search(query))
        info = self.ydl.extract_info(videoId)
        filename = self.ydl.prepare_filename(info)
        return (info['fulltitle'], filename, discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, options='-vn')))
