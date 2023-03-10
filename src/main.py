import discord, os
from discord.ext import commands

BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
prefix = '>'

class DokkaebiClient(commands.Bot):
    def __init__(self):
        # define intent
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix = prefix,
            intents = intents
        )

    async def on_ready(self):
        print('Dokkaebi bot is ready to roll')

    async def setup_hook(self):
        return await self.load_cogs()
    
    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                await self.tree.sync()

    '''
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
    '''


client = DokkaebiClient()
client.run(BOT_TOKEN)