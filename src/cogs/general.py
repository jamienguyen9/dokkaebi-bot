import discord, os
from discord import app_commands
from discord.ext import commands

class General_Commands(commands.Cog):
    '''Cog for general commands.'''

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name = 'reload', description = 'Reloads cogs - used for debugging purposes')
    async def reload(self, interaction: discord.Interaction) -> None:
        """Reloads all cog files"""
        for filename in os.listdir('/cogs'):
            if filename.endswith('.py'):
                await self.reload_extension(f'cogs.{filename[:-3]}')
                await self.tree.sync()


async def setup(bot: commands.Bot):
    await bot.add_cog(General_Commands(bot))