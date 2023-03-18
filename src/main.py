import discord, os
from discord.ext import commands
from discord import app_commands


BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
prefix = '>'

class DokkaebiClient(commands.Bot):
    """Discord Bot Client"""

    def __init__(self):
        # define intent
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix = prefix,
            intents = intents
        )

    async def on_ready(self) -> None:
        print('Dokkaebi bot is ready to roll')

    async def setup_hook(self) -> None:
        return await self.load_cogs()
    
    async def load_cogs(self) -> None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                await self.tree.sync()

    @app_commands.command(name = 'reload', description = 'Reloads new cogs')
    async def reload(self) -> None:
        """Reloads all cog files"""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.reload_extension(f'cogs.{filename[:-3]}')
                await self.tree.sync()


client = DokkaebiClient()
client.run(BOT_TOKEN)