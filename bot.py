import discord
from discord.errors import LoginFailure
from discord.ext import commands
import asyncio, os
from dotenv import load_dotenv
from youtube import YoutubeStream

load_dotenv()

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yts = YoutubeStream()

    @commands.command()
    async def play(self, ctx, query):
        async with ctx.typing():
            try:
                song, file, source = await self.yts.stream(query, loop=self.bot.loop)
            except ValueError as e:
                await ctx.send(str(e))
                raise commands.CommandError(str(e))
            self.current_file = file
            ctx.voice_client.play(source, after=lambda e:self._end_song(e))
        await ctx.send(f'Now playing: {song}')

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Not connected to a voice channel")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    def _end_song(self, e):
        if e:
            print(f'Player error: {e}')
        if os.path.exists(self.current_file):
            os.remove(self.current_file)
        self.current_file = ""

intents = discord.Intents().default()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv("command_prefix"), intents=intents)

async def main():
    async with bot:
        await bot.add_cog(Player(bot))
        token = os.getenv('discord_token')
        try:
            await bot.start(token)
        except LoginFailure as e:
            print(str(e))
            raise e

if __name__ == '__main__':
    asyncio.run(main())
