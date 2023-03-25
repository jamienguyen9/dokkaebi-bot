import re
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

def poke_info(pokemon_info : dict, pokedex_entry : dict) -> Embed:
    embed = Embed(
        color = Colour.red(),
        title = pokemon_info['name'].capitalize(),
        description = re.sub('[^A-Za-z0-9]+', ' ', pokedex_entry['flavor_text_entries'][0]['flavor_text'])
    )
    embed.set_thumbnail(url = pokemon_info['sprites']['front_default'])
    embed.add_field(name = 'Pokedex Number', value = str(pokemon_info['id']).zfill(4), inline = True)
    
    types = ''
    for type_info in pokemon_info['types']:
        if not types:
            types = type_info['type']['name'].capitalize()
        else:
            types = types + ' / ' + type_info['type']['name'].capitalize()
    embed.add_field(name = 'Types', value = types, inline = True)
    embed.add_field(name = "\u200B", value = "\u200B")
    
    height = str(pokemon_info['height'] / 10.0) + ' m'
    weight = str(pokemon_info['weight'] / 10.0) + ' kg'

    embed.add_field(name = 'Height', value = height, inline = True)
    embed.add_field(name = 'Weight', value = weight, inline = True)
    embed.add_field(name = 'Catch Rate', value = pokedex_entry['capture_rate'], inline = True)

    abilities = ''
    for ability_info in pokemon_info['abilities']:
        if not abilities:
            abilities = ability_info['ability']['name'].capitalize()
        else:
            abilities = abilities + ', ' + ability_info['ability']['name'].capitalize()
        if ability_info['is_hidden']:
            abilities = abilities + ' (hidden)'
    embed.add_field(name = 'Abilities', value = abilities, inline = False)


    return embed

def cannot_find_poke_info() -> Embed:
    embed = Embed(
        color = Colour.red(),
        title = 'Cannot find information with the input entered. Please try again.'
    )
    return embed