
# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$josef'):
        await message.channel.send('https://cdn.discordapp.com/attachments/970994367441534996/971022925928992818/unknown.png')

    if 'oscar' in message.content:
        await message.channel.send('Fuck the Oscars!')

client.run(TOKEN)
