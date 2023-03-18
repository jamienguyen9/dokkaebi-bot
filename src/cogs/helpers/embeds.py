from discord import Embed
from discord import Colour

def now_playing(song: dict) -> Embed:
    embed = Embed(
        color = Colour.purple(),
        title = 'Now Playing:',
        description = '`{}`'.format(song['title']),
        url = song['url']
    )
    embed.set_thumbnail(url = song['thumbnail'])
    embed.add_field(name = 'Requested By', value = song['requestor'], inline = True)
    embed.add_field(name = 'Song By', value = song['author'], inline = True)
    embed.add_field(name = 'Duration', value = '`{}`'.format(song['duration']), inline = True)
    return embed

def add_to_queue(song: dict, song_queue: list) -> Embed:
    embed = Embed(
        color = Colour.purple(),
        title = 'Added to Queue:',
        description = '`{}`'.format(song['title']),
        url = song['url']
    )
    embed.set_thumbnail(url = song['thumbnail'])
    embed.add_field(name = 'Added By', value = song['requestor'], inline = True)
    embed.add_field(name = 'Song By', value = song['author'], inline = True)
    embed.add_field(name = 'Position in Queue', value = '`{}`'.format(len(song_queue)), inline = True)
    return embed

def no_more_song() -> Embed:
    embed = Embed(
        color = Colour.purple(),
        title = 'Queue has ended. No more songs left to play'
    )
    return embed

def no_songs() -> Embed:
    embed = Embed(
        color = Colour.purple(),
        title = 'There are no songs in the queue'
    )
    return embed
                
def removed_song(song: str) -> Embed:
    embed = Embed(
        color = Colour.purple(),
        title = 'Removed song: `{}`'.format(song)
    )
    return embed

def leaving_channel_idle() -> Embed:
    embed = Embed(
        color = Colour.purple(),
        title = 'No more songs in the queue. Leaving channel...'
    )
    return embed