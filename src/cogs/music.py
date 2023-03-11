import discord, urllib.parse, urllib.request, re
from discord import app_commands
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):

    YDL_OPTS = {'format': 'bestaudio/best'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
        'options': '-vn'
    }

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @app_commands.command(name = "play", description= "Play a song")
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        voice_state = interaction.user.voice
        print(self.download_song(query))

        if voice_state:
            voice_channel = voice_state.channel
            audio_client = await voice_channel.connect()

            song = self.download_song(query)
            
            audio_source = discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS)

            audio_client.play(audio_source, after = None)
        else:
            print("You are not in a voice channel. Please join one to play music.")
        

    def download_song(self, query):
        video_prefix = 'https://www.youtube.com/watch?v='
        result_prefix = 'https://www.youtube.com/results?'
        result_suffix = urllib.parse.urlencode({
            'search_query' : query
        })

        search_results = urllib.request.urlopen(result_prefix + result_suffix)
        video_suffix = re.findall(r'watch\?v=(\S{11})', search_results.read().decode())[0]
        url = video_prefix + video_suffix

        with YoutubeDL(Music.YDL_OPTS) as ydl:
            song = ydl.extract_info(url, download=False)
        
        return {
            'title': song['title'],
            'author': song['uploader'],
            'source': song['formats'][0],
            'duration': song['duration'],
            'thumbnail': song['thumbnail']
        }
        
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
