from email.policy import default
import discord
import os
from discord import app_commands
from jellyapiclient import Jellyapi
import enum
from formula import FormulaFeature
import json
from typing import Literal, List
import streams
from discord.ext import tasks
import configparser


def CreateSettingsIni():
    try:
        file = open("settings.conf", "x")
    except:
        print("Settings found.")
        return
    filetext = "[BOT]\nDiscordToken =\nJellyApi =\nJellyAddress =\nBot_UID =\nDiscordServerID =\nStreamIP= "
    file.write(filetext)
    print("File created. Fill the settings file.")
    exit(2)

def LoadSettings():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    config.sections()
    return config

CreateSettingsIni()
settings = LoadSettings()

API_KEY = settings['BOT']['JellyApi']
ADDRESS = settings['BOT']['JellyAddress']
JELLY_UID = settings['BOT']['Bot_UID']
TOKEN = settings['BOT']['DiscordToken']
SERVER_ID = settings['BOT']['DiscordServerID']
STREAM_URL = settings['BOT']['StreamIP']


if not API_KEY or not ADDRESS or not JELLY_UID or not TOKEN or not SERVER_ID or not STREAM_URL:
    print("Missing settings values")
    exit(3)


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
jellyClient = Jellyapi(ADDRESS,API_KEY,JELLY_UID)


jsonDict = json.load(open('f1times.json'))
GPList = FormulaFeature.GetAllGPs(jsonDict)

LibList = []
for x in jellyClient.GetAllLibs().Items:
    LibList.append(str(x.Name))

LibEnum = enum.Enum('Lib', LibList)

@tree.command(name = "hello", description = "Say Hello", guild=discord.Object(id=SERVER_ID)) 
async def hello_command(interaction):
    await interaction.response.send_message("Hello, " + interaction.user.name + "!")

@tree.command(name= "help", description = "Prints help message",guild=discord.Object(id=SERVER_ID))
async def helpcommand(interaction):
    msg = "Hey, " + interaction.user.name + "!\n These are commands you can use with this bot:\n```\\hello\n\\f1\n\\jelly```"
    await interaction.response.send_message(msg)

@tree.command(name = "jelly", description= "Jellyfin commands", guild=discord.Object(id=SERVER_ID), )
async def jellyLibs(interaction, library:LibEnum):
    lib = jellyClient.GetLibByName(str(library.name))
    item = jellyClient.GetLibraryItems(lib.Id)
    itemList = ""

    for x in item.Items:
        itemList+=x.Name + "\n"

    await interaction.response.send_message(str(itemList))

@tree.command(name = "f1", description= "F1 commands", guild=discord.Object(id=SERVER_ID))
async def F1Command(interaction, option:str, option2:str=None):
    if option == "when":
         await interaction.response.send_message(FormulaFeature.FindClosestSession(jsonDict, option2))
         return
       
    if option == "gp":
        res = FormulaFeature.GetGPByName(jsonDict, str(option2))

        if not res:
            await interaction.response.send_message("Incorrect argument provided. Try again with correct arguments")
            return
        
        sessionString = ""
        
        results = FormulaFeature.GetRaceStandingsByRound(int(res.Round))
        for x in res.Sessions:
            sessionString += "{sessionName} @ {sessionTime}\n".format(sessionName = x.Name, sessionTime = FormulaFeature.GetFormattedSessionTime(x, None))
    
        response = "__**Round {roundnr} - {GPName}**__ \nSessions:\n{sessionList}".format(roundnr = res.Round, GPName = res.Name, sessionList = sessionString)

        if results != None:
            response += "\n__**:checkered_flag:Results::checkered_flag:**__"
            for x in results.Results:
                response += "\n{position}. {firstName} {lastName} - {points}".format(position=x.position, firstName=x.Driver.givenName, lastName=x.Driver.familyName, points=x.points)
        await interaction.response.send_message(response)
        return
    
    if option == "standings":
        
        standings = FormulaFeature.GetStandings()
        result = "Season {seasonYear}:\n".format(seasonYear = standings.season)
        for x in standings.StandingsLists[0].DriverStandings:
            result += "{pos}. {driverName} {points}\n".format(pos = x.position, driverName = x.Driver.familyName, points = x.points)

        await interaction.response.send_message(result)
        return
    
    await interaction.response.send_message("Wrong command")
                    
    

@F1Command.autocomplete('option')
async def F1WhenAutocomplete(
    interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
    options = ['when', 'standings', 'gp']
    return [
        app_commands.Choice(name=option, value=option)
        for option in options if current.lower() in option.lower()
    ]
@F1Command.autocomplete('option2')
async def F1WhenAutocomplete(
    interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
    options = GPList
    print(current, interaction.namespace['option'])
    if interaction.namespace['option'] == 'when':
        return []
    if interaction.namespace['option'] == 'gp':
        return [
            app_commands.Choice(name=option.Name, value=option.Name)
            for option in options if current.lower() in option.Name.lower()
        ]



@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f'We have logged in as {client.user}')
    print("Ready!")
    #RunStreamCheck.start()
   
#reactions to messages without slash    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'oscar' in message.content.lower():
        print("oscar detected")
        await message.channel.send('Fuck the Oscars!')

client.run(TOKEN)
