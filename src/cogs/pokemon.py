import discord, requests
from discord import app_commands
from discord.ext import commands
from cogs.helpers import embeds

class Pokemon_Info(commands.Cog):
    """Pokemon Cog"""

    BASE_URL = 'https://pokeapi.co/api/v2/'
    BASE_DEX_URL = 'https://pokeapi.co/api/v2/pokemon-species/'

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name = 'poke_info', description = 'Get information on a pokemon')
    async def poke_info(self, interaction: discord.Interaction, pokemon_or_id: str) -> None:
        """Retrieves information on a pokemon based on the given pokemon name or id
        
        ### Parameters
        `pokemon_or_id` : pokemon name or id that the user entered
        """
        info_response = None
        dex_response = None
        try:
            # TODO: add try/catch exception to prevent 404s
            info_response = requests.get(Pokemon_Info.BASE_URL + 'pokemon/{}/'.format(pokemon_or_id))
            dex_response = requests.get(Pokemon_Info.BASE_DEX_URL + 'pokemon/{}/'.format(pokemon_or_id))
        except requests.exceptions.HTTPError as err:
            print(err)
        finally:
            if info_response and dex_response and info_response.status_code == 200 and dex_response == 200:
                pokeinfo = info_response.json()
                dexinfo = dex_response.json()

                embed = embeds.poke_info(pokeinfo, dexinfo)
                await interaction.response.send_message(embed = embed)
            else:
                await interaction.response.send_message(embed = embeds.cannot_find_poke_info())
    

    @app_commands.command(name = 'poke_item', description = 'Get information on a pokemon item')
    async def poke_item(self, interaction: discord.Interaction, item_or_id: str) -> None:
        pass


    @app_commands.command(name = 'poke_evolution', description = 'Get information on a pokemon evolution')
    async def poke_evolution(self, interaction: discord.Interaction, pokemon_or_id: str) -> None:
        pass

    @app_commands.command(name = 'poke_ability', description = 'Get information on a pokemon ability')
    async def poke_ability(self, interaction: discord.Interaction, pokemon_or_id: str) -> None:
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Pokemon_Info(bot))