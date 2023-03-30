import discord
from discord import app_commands
from jellyapiclient import Jellyapi
import enum
from formula import FormulaFeature
import json
from typing import List
from discord.ext import tasks
import configparser
import requests



def load_settings():
    config = configparser.ConfigParser()

    try:
        config_file = open('settings.conf', 'r')
    except OSError:
        config['BOT'] = {"Discord_Token" : '',
                         'Jelly_API': '',
                         'Jelly_Address': '',
                         'Bot_UID': '',
                         'Discord_ServerID': '',
                         'Stream_IP' : '',
                         'F1_Calendar_Json': '',
                         'Under_Surveilance': ''}
        with open('settings.conf', 'w') as config_file:
            config.write(config_file)
        print("Settings file not found. Template settings file was created.")
        exit(2)



    config.read('settings.conf')
    config.sections()
    return config

settings = load_settings()


try:
    API_KEY = settings['BOT']['Jelly_Api']
    ADDRESS = settings['BOT']['Jelly_Address']
    JELLY_UID = settings['BOT']['Bot_UID']
    TOKEN = settings['BOT']['Discord_Token']
    SERVER_ID = settings['BOT']['Discord_ServerID']
    STREAM_URL = settings['BOT']['Stream_IP']
    CALENDAR_JSON = settings['BOT']['F1_Calendar_Json']
except KeyError as e:
    print("Missing config line")
    exit(4)

surveilance_target = settings['BOT']['Under_Surveilance'].split(',')

if not API_KEY or not ADDRESS or not JELLY_UID or not TOKEN or not SERVER_ID or not STREAM_URL:
    print("Missing settings values")
    exit(3)


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
jellyClient = Jellyapi(ADDRESS,API_KEY,JELLY_UID)

try:
    json_data = requests.get(CALENDAR_JSON).content
except:
    try:
        json_data = open(CALENDAR_JSON, 'r').read()
    except OSError:
        print("Invalid calendar JSON location. Use URL or path to the file")
        exit(4)
try:
    json_dict = json.loads(json_data)
except:
    print("Error in calendar json file")
    exit(1)
gp_list = FormulaFeature.get_all_gps(json_dict)

lib_list = []
for x in jellyClient.get_all_libs().Items:
    lib_list.append(str(x.name))

lib_enum = enum.Enum('Lib', lib_list)

@tree.command(name = "surveil", description = "Setup survailane target", guild=discord.Object(id=SERVER_ID)) 
async def surveil(interaction, option:str):
    global surveilance_target
    surveilance_target = option.split(',')
    await interaction.response.send_message("Setting changed")


@tree.command(name = "hello", description = "Says Hello to user", guild=discord.Object(id=SERVER_ID)) 
async def hello_command(interaction):

    await interaction.response.send_message("Hello, " + interaction.user.name + "!")

@tree.command(name= "help", description = "Shows availible commands with their description",guild=discord.Object(id=SERVER_ID))
async def help_command(interaction):

    msg = interaction.user.name+", bot currently supports these commands:\n\n"

    for com in tree.walk_commands(guild=discord.Object(id=SERVER_ID)):
        msg += "**\\"+com.name+"**\n\t"+com.description+"\n\n"

    await interaction.response.send_message(content = msg, ephemeral=True)

@tree.command(name= "issues", description = "Link to add/view known issues on GitHub",guild=discord.Object(id=SERVER_ID))
async def issue_command(interaction):

    issues_link = 'https://github.com/dasno/movie_bot/issues'
    msg = "You can post/review bot issues here:\n"+issues_link

    await interaction.response.send_message(content = msg, ephemeral=True)

@tree.command(name = "jelly", description= "Commands to utilize Jellyfin server library", guild=discord.Object(id=SERVER_ID), )
async def jelly_libs(interaction, library:lib_enum):

    lib = jellyClient.get_lib_by_name(str(library.name))
    item = jellyClient.get_library_items(lib.id)
    itemList = ""

    for x in item.Items:
        itemList+=x.Name + "\n"

    await interaction.response.send_message(str(itemList))

@tree.command(name = "f1", description= "Commands to show race results, standings and upcoming F1 races", guild=discord.Object(id=SERVER_ID))
async def f1_command(interaction, option:str, option2:str=None):

    if option == "when":
         gp,session = FormulaFeature.find_closest_session(json_dict)
         response = "Closest session is **{gp} {session_name}** @ {session_start}".format(session_name=session.Name,
                                                                                          session_start=FormulaFeature.get_formatted_session_time(session, option2),
                                                                                          gp=gp.Name)
         if FormulaFeature.is_ongoing(session):
             response += "\n:red_circle: **Session is live**"
         await interaction.response.send_message(response)
         return
       
    if option == "gp":
        res = FormulaFeature.get_gp_by_name(json_dict, str(option2))

        if not res and option2 != None:
            await interaction.response.send_message("Incorrect argument provided. Try again with correct arguments")
            return
        
        if not option2:
            race = FormulaFeature.find_closest_past_race(json_dict)
            result = FormulaFeature.get_latest_results(json_dict)
            response =  """Last race was **{raceName}** on {raceDate}\n\n__**:checkered_flag:Results::checkered_flag:**__
            {results}
            """.format(raceName = race.Name, raceDate = race.Sessions[4].StartTime.date().strftime("%d.%m.%Y"), results = FormulaFeature.format_results(result))
            await interaction.response.send_message(response)
            return

        
        sessionString = ""
        
        results = FormulaFeature.get_race_results_by_round(int(res.Round))
        for x in res.Sessions:
            sessionString += "{sessionName} @ {sessionTime}\n".format(sessionName = x.Name, sessionTime = FormulaFeature.get_formatted_session_time(x, None))
    
        response = "__**Round {roundnr} - {GPName}**__ \nSessions:\n{sessionList}".format(roundnr = res.Round, GPName = res.Name, sessionList = sessionString)
        
        e = discord.Embed()
        e.set_image(url=res.Map)

        if results != None:
            response += "\n__**:checkered_flag:Results::checkered_flag:**__"
            response += FormulaFeature.format_results(results.Results)
        
        await interaction.response.send_message(response, embed=e)
        
        return
    
    if option == "standings":
        
        if option2 == None or option2 == "drivers":
            standings = FormulaFeature.get_driver_standings()
            result = "**{seasonYear} Driver Standings**:\n".format(seasonYear = standings.season)
            for x in standings.StandingsLists[0].DriverStandings:
                result += "{pos}. {driverName} - {points}\n".format(pos = x.position, driverName = x.Driver.familyName, points = x.points)
        else:
            standings = FormulaFeature.get_constructor_standings()
            result = "**{seasonYear} Constructor Standings**:\n".format(seasonYear = standings.season)
            for x in standings.StandingsLists[0].ConstructorStandings:
                result += "{pos}. {constructor} - {points}\n".format(pos = x.position, constructor = x.Constructor.name, points = x.points)
        await interaction.response.send_message(result)
        return
    
    await interaction.response.send_message("Wrong command")
                    
    

@f1_command.autocomplete('option')
async def f1_when_autocomplete(
    interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
    options = ['when', 'standings', 'gp']
    return [
        app_commands.Choice(name=option, value=option)
        for option in options if current.lower() in option.lower()
    ]
@f1_command.autocomplete('option2')
async def f1_when_autocomplete(
    interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
    options = gp_list
    print(current, interaction.namespace['option'])
    if interaction.namespace['option'] == 'when':
        return []
    if interaction.namespace['option'] == 'gp':
        return [
            app_commands.Choice(name=option.Name, value=option.Name)
            for option in options if current.lower() in option.Name.lower()
        ]
    if interaction.namespace['option'] == "standings":
        options = ["driver", "constructor"]
        return [app_commands.Choice(name=option, value = option) for option in options]




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
    


@client.event
async def on_message_delete(message):
    if str(message.author.id) in surveilance_target:
        await message.channel.send("<:reverse:1090742023801286777> {usr}: {msg}".format(msg=message.content,
                                                                                        usr=message.author.mention))

client.run(TOKEN)
