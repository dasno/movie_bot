
#test lol

from email.policy import default
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

    

    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$josef'):
        await message.channel.send('https://cdn.discordapp.com/attachments/970994367441534996/971022925928992818/unknown.png')

    if 'oscar' in message.content.lower():
        await message.channel.send('Fuck the Oscars!')
    if message.content.startswith('$jelly'):
        await JellyCommand(message)


async def JellyCommand(message):
    command = message.content.split()
    if (len(command) < 2):
        await message.channel.send('Help command placeholder')
    print(command)
    match command[1]:
        case 'help':
            await message.channel.send('Help command placeholder')
        case 'list':
            await JellyListCommand(message, command)
        case _:
            await message.channel.send('Command not found')

async def JellyListCommand(message, command):
    if (len(command) < 3):
        await message.channel.send('List subcommand help placeholder')
    match command[2]:
        case 'libs':
            await message.channel.send('List all libraries placeholder')
        case _:
            #TODO detect valid libraries or throw some error
            pass

client.run(TOKEN)
