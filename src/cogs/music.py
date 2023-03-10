import discord
from discord import app_commands
from discord.ext import commands

class Music(commands.Cog):

    YDL_OPTS = {'format': 'bestaudio/best'}


    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @app_commands.command(name = "play", description= "Play a song")
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        # TODO
        print(query)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
