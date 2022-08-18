from ast import keyword
from sqlite3 import connect
from xml.etree.ElementTree import tostring
from Classes.Connection import Connection
from Classes.AllLibs import AllLibs
from Classes.LibraryItems import LibraryItems
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('JELLY_KEY')
ADDRESS = os.getenv('ADDRESS')
#TODO get all defualt bot userId from env file


con = Connection(API_KEY, ADDRESS)

def GetAllLibs(connection: Connection):
    header = {'X-Emby-Token':API_KEY}
    target = connection.Address + "/Items"
    response = requests.get(target,
                            headers=header,
                            params={'userId':'2ae057263010412386af9d21168de268'})
    resJson = json.loads(response.content)
    return AllLibs.from_dict(resJson)


def GetLibraryItems(connection: Connection, libId):
    header = {'X-Emby-Token':API_KEY}
    target = connection.Address + "/Items"
    response = requests.get(target,
                            headers=header,
                            params= {'userId':'2ae057263010412386af9d21168de268',
                                    'parentId' : libId})
    resJson = json.loads(response.content)
    return LibraryItems.from_dict(resJson)

def GetLibByName(con:Connection, libname):
    libs = GetAllLibs(con)
    lib = None
    for i in libs.Items:
        if(i.Name == libname):
            lib = i
            break
    return lib



lib = GetLibByName(con, "Movies")
items = GetLibraryItems(con, str(lib.Id))
for i in items.Items:
    print(i.Name)

        
