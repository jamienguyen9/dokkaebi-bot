import discord, urllib.parse, urllib.request, re, asyncio, datetime, sys
from discord import app_commands
from discord.ext import commands
from youtube_dl import YoutubeDL
from cogs.helpers import embeds

class Music(commands.Cog):
    """Music Cog"""

    YDL_OPTIONS = {'format': 'bestaudio/best'}
    FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }


    def __init__(self, bot) -> None:
        self.bot = bot
        self.audio_client: discord.VoiceClient = None
        self.song_queue = []
        self.event_loop = asyncio.get_event_loop()


    @app_commands.command(name = 'play', description = 'Play a song')
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        """Joins the user's voice channel and plays audio.
        
        ### Parameters
        `interaction` : A discord interaction object
        """
        voice_state = interaction.user.voice

        # Check if user is in voice channel
        if voice_state:
            voice_channel = voice_state.channel
            if self.audio_client is None:
                self.audio_client = await voice_channel.connect()
            elif voice_channel.id != self.audio_client.channel.id:
                content = "You and the bot are in difference voice channels. Please join its channel to play a song"
                await interaction.response.send_message(content = content)
                return

            # Download Song
            song = self.download_song(query)
            song['requestor'] = interaction.user.mention
            self.song_queue.append(song)        
            
            # Check if client is currently playing audio
            if self.audio_client.is_playing():
                await interaction.response.send_message(embed = embeds.add_to_queue(song, self.song_queue))
            else:
                song = self.song_queue.pop(0)
                await interaction.response.send_message(embed = embeds.now_playing(song))
                audio_source = discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS)
                self.audio_client.play(audio_source, after = lambda e: self.play_next(interaction))
                
        else:
            content = "You are not in a voice channel. Please join one to play music."
            await interaction.response.send_message(content = content)


    @app_commands.command(name = 'skip', description = 'Skip the current song')
    async def skip(self, interaction: discord.Interaction) -> None:
        """Stops the current audio and plays the next song in the song queue.

        ### Parameters
        `interaction` : A discord interaction object
        """
        voice_state = interaction.user.voice
        if voice_state:
            if not self.song_queue:
                embed = embeds.no_more_song()
                await interaction.response.send_message(embed = embed)
            else:
                # stop() stops the client from playing audio then calls play_next() again
                self.audio_client.stop()
                await interaction.response.send_message(content="Skipping song...")


    @app_commands.command(name = 'queue', description = "View the song queue")
    async def queue(self, interaction: discord.Interaction) -> None:
        """Views a list of songs that are next in the queue.
        
        ### Parameters
        `interaction` : A discord interaction object
        """
        if not self.song_queue:
            await interaction.response.send_message(embed = embeds.no_songs())
            return
        embed = discord.Embed(
            color = discord.Colour.purple(),
            title = 'Up Next:',
        )
        for i, item in enumerate(self.song_queue):
            embed.add_field(name = '{}. `{}`'.format(i + 1, item['title']), value = '', inline = False)
        await interaction.response.send_message(embed = embed)


    @app_commands.command(name = 'remove', description = 'Remove a song in the queue')
    async def remove(self, interaction: discord.Interaction, position: int) -> None:
        """Removes a song in the queue based on the position
        
        ### Parameters
        `interaction` : A discord interaction object
        `position` : Position of the song that you want to remove
        """
        if not self.song_queue:
            await interaction.response.send_message(embed = embeds.no_songs())
            return
        if position > len(self.song_queue):
            await interaction.response.send_message(content = 'The position you entered does not work. Please try again')
            return
        song_title = self.song_queue.pop(position - 1)['title']
        await interaction.response.send_message(embed = embeds.removed_song(song_title))


    @app_commands.command(name = 'leave', description = 'Leave the voice channel')
    async def leave(self, interaction: discord.Interaction) -> None:
        """Stops playing audio then leaves the channel
        
        ### Parameters
        `interaction` : A discord interaction object
        """
        self.song_queue.clear()
        await self.audio_client.disconnect()
        await interaction.response.send_message(content = 'Leaving Channel.')
    
    
    def play_next(self, interaction: discord.Interaction) -> None:
        """Plays the next song in the queue
        
        ### Parameters
        `interaction` : A discord interaction object
        """
        if self.song_queue:
            song = self.song_queue.pop(0)
            audio_source = discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS)
            self.audio_client.play(audio_source, after = lambda e: self.play_next(interaction))
            asyncio.run_coroutine_threadsafe(interaction.channel.send(embed = embeds.now_playing(song)), self.event_loop)
        else:
            if not self.audio_client.is_playing():
                asyncio.run_coroutine_threadsafe(self.audio_client.disconnect(), self.event_loop)
                self.audio_client = None
                asyncio.run_coroutine_threadsafe(interaction.channel.send(embed = embeds.leaving_channel_idle()), self.event_loop)


    def download_song(self, query: str) -> dict:
        """Downloads the first result of a youtube video based on the search query
        
        ### Parameters
        `query` : search query that the user entered
        """
        video_prefix = 'https://www.youtube.com/watch?v='
        result_prefix = 'https://www.youtube.com/results?'
        result_suffix = urllib.parse.urlencode({
            'search_query' : query
        })

        search_results = urllib.request.urlopen(result_prefix + result_suffix)
        video_suffix = re.findall(r'watch\?v=(\S{11})', search_results.read().decode())[0]
        url = video_prefix + video_suffix

        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            song = ydl.extract_info(url, download=False)

        # Truncates the duration string to be a bit more readable if the song is less than an hour
        duration = str(datetime.timedelta(seconds = song['duration']))
        index = 0
        if int(duration[:1]) == 0:
            index = 2
        elif int(duration[2:3]) == 0:
            index = 3
        duration = duration[index:]
        
        return {
            'url': url,
            'title': song['title'],
            'author': song['uploader'],
            'source': song['formats'][0]['url'],
            'duration': duration,
            'thumbnail': song['thumbnail'],
            'requestor': None
        }
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))