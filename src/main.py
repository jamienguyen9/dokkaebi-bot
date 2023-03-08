import discord, os

BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print('Dokkaebi bot is ready to roll')

client.run(BOT_TOKEN)