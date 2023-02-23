from email.policy import default
import discord
from dotenv import load_dotenv
import os
from discord import app_commands
from jellyapiclient import Jellyapi
import enum

load_dotenv()

API_KEY = os.getenv('JELLY_KEY')
ADDRESS = os.getenv('ADDRESS')
JELLY_UID = os.getenv('JELLY_BOT_UID')
#TODO get all defualt bot userId from env file
TOKEN = os.getenv('BOT_TOKEN')
SERVER_ID = os.getenv('DISCORD_SERVER_ID')
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
jellyClient = Jellyapi(ADDRESS,API_KEY,JELLY_UID)

LibList = []
for x in jellyClient.GetAllLibs().Items:
    LibList.append(str(x.Name))

LibEnum = enum.Enum('Lib', LibList)
print(list)          
@tree.command(name = "hello", description = "Say Hello", guild=discord.Object(id=SERVER_ID)) 
async def hello_command(interaction):
    await interaction.response.send_message("Hello, " + interaction.user.name + "!")

@tree.command(name = "jelly", description= "Jellyfin commands", guild=discord.Object(id=SERVER_ID))
async def jellyLibs(interaction, subcommand:LibEnum):
    lib = jellyClient.GetLibByName(str(subcommand.name))
    item = jellyClient.GetLibraryItems(lib.Id)
    itemList = ""
    for x in item.Items:
        itemList+=x.Name + "\n"
    await interaction.response.send_message(str(itemList))

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f'We have logged in as {client.user}')
    print("Ready!")
   
#reactions to messages without slash    
@client.event
async def on_message(message):
    print("Msg detected")
    print(message.content)
    if message.author == client.user:
        return

    if 'oscar' in message.content.lower():
        print("oscar detected")
        await message.channel.send('Fuck the Oscars!')

client.run(TOKEN)
