import discord, urllib.parse, urllib.request, re, asyncio, datetime
from discord import app_commands
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):

    YDL_OPTIONS = {'format': 'bestaudio/best'}
    FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }

    def __init__(self, bot):
        self.bot = bot
        self.audio_client = None
        self.song_queue = []
        self.event_loop = asyncio.get_event_loop()

    @app_commands.command(name = 'play', description= 'Play a song')
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        voice_state = interaction.user.voice

        # Check if user is in voice channel
        if voice_state:
            voice_channel = voice_state.channel
            if self.audio_client is None:
                self.audio_client = await voice_channel.connect()

            #TODO create case where two people are using the bot in different channels

            # Download Song
            song = self.download_song(query)
            song['requestor'] = interaction.user.mention
            self.song_queue.append(song)        
            
            # Check if client is currently playing audio
            if self.audio_client.is_playing():
                await interaction.response.send_message(embed = self.embed_add_to_queue(song))
            else:
                song = self.song_queue.pop(0)
                audio_source = discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS)
                self.audio_client.play(audio_source, after = lambda e: self.play_next(interaction))
                await interaction.response.send_message(embed = self.embed_now_playing(song))
        else:
            print("You are not in a voice channel. Please join one to play music.")
        
    @app_commands.command(name = 'skip', description= 'Skip the current song')
    async def skip(self, interaction: discord.Interaction) -> None:
        voice_state = interaction.user.voice
        if voice_state:
            if not self.song_queue:
                embed = self.embed_no_more_song()
                await interaction.response.send_message(embed = embed)
            else:
                await self.audio_client.stop()
                await interaction.response.send_message(content="Skipping song...")
                self.play_next(interaction)

    @app_commands.command(name = 'queue', description = "View the song queue")
    async def queue(self, interaction: discord.Interaction) -> None:
        if not self.song_queue:
            await interaction.response.send_message(embed = self.embed_no_songs())
            return
        embed = discord.Embed(
            color = discord.Colour.purple(),
            title = 'Up Next:',
        )
        for i, item in enumerate(self.song_queue):
            embed.add_field(name = '{}. `{}`'.format(i, item['title']), value = '', inline = False)
        await interaction.response.send_message(embed = embed)

    @app_commands.command(name = 'remove', description = 'Remove a song in the queue')
    async def remove(self, interaction: discord.Interaction, position : int) -> None:
        if not self.song_queue:
            await interaction.response.send_message(embed = self.embed_no_songs())
            return
        if position > len(self.song_queue):
            await interaction.response.send_message(content = 'The position you entered is not in this queue. Please try again')
            return
        song = self.song_queue.pop(position - 1)['title']
        await interaction.response.send_message(embed = self.embed_removed_song(song))


    def play_next(self, interaction: discord.Interaction):
        if self.song_queue:
            song = self.song_queue.pop(0)
            print(list)
            audio_source = discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS)
            self.audio_client.play(audio_source, after = lambda e: self.play_next(interaction))
            asyncio.run_coroutine_threadsafe(interaction.channel.send(embed = self.embed_now_playing(song)), self.event_loop)
        else:
            if not self.audio_client.is_playing():
                asyncio.run_coroutine_threadsafe(self.audio_client.disconnect(), self.event_loop)
                self.audio_client = None
                asyncio.run_coroutine_threadsafe(interaction.channel.send(embed = self.embed_leaving_channel_idle()), self.event_loop)

    def download_song(self, query : str):
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
    
    def embed_now_playing(self, song : dict):
        embed = discord.Embed(
            color = discord.Colour.purple(),
            title = 'Now Playing:',
            description = '`{}`'.format(song['title']),
            url = song['url']
        )
        embed.set_thumbnail(url = song['thumbnail'])
        embed.add_field(name = 'Requested By', value = song['requestor'], inline = True)
        embed.add_field(name = 'Song By', value = song['author'], inline = True)
        embed.add_field(name = 'Duration', value = '`{}`'.format(song['duration']), inline = True)
        return embed
    
    def embed_add_to_queue(self, song : dict):
        embed = discord.Embed(
            color = discord.Colour.purple(),
            title = 'Added to Queue:',
            description = '`{}`'.format(song['title']),
            url = song['url']
        )
        embed.set_thumbnail(url = song['thumbnail'])
        embed.add_field(name = 'Added By', value = song['requestor'], inline = True)
        embed.add_field(name = 'Song By', value = song['author'], inline = True)
        embed.add_field(name = 'Position in Queue', value = '`{}`'.format(len(self.song_queue)), inline = True)
        return embed
    
    def embed_no_more_song(self):
        embed = discord.Embed(
            color = discord.Colour.purple(),
            title = 'Queue has ended. No more songs left to play'
        )
        return embed
    
    def embed_no_songs(self):
        embed = discord.Embed(
            color = discord.Color.purple(),
            title = 'There are no songs in the queue'
        )
        return embed
                    
    def embed_removed_song(self, song : str):
        embed = discord.Embed(
            color = discord.Color.purple(),
            title = 'Removed song: {}'.format(song)
        )
        return embed
    
    def embed_leaving_channel_idle(self):
        embed = discord.Embed(
            color = discord.Colour.purple(),
            title = 'No more songs in the queue. Leaving channel...'
        )
        return embed
        
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
