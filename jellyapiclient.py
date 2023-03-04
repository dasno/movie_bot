from ast import keyword
from sqlite3 import connect
from xml.etree.ElementTree import tostring
from Classes.Connection import Connection
from Classes.AllLibs import AllLibs
from Classes.LibraryItems import LibraryItems
import json
import requests


class Jellyapi:
    
    def __init__(self, jellyAddress, jellyAPI, jellyUID):
        self.API_KEY = jellyAPI
        self.ADDRESS = jellyAddress
        self.JELLY_UID = jellyUID
        self.con = Connection(self.API_KEY, self.ADDRESS)


    def GetAllLibs(self):
        header = {'X-Emby-Token':self.API_KEY}
        target = self.con.Address + "/Items"
        response = requests.get(target,
                                headers=header,
                                params={'userId':self.JELLY_UID})
        resJson = json.loads(response.content)
        return AllLibs.from_dict(resJson)

    def GetLibraryItems(self, libId):
        header = {'X-Emby-Token':self.API_KEY}
        target = self.con.Address + "/Items"
        response = requests.get(target,
                                headers=header,
                                params= {'userId':self.JELLY_UID,
                                        'parentId' : libId})
        resJson = json.loads(response.content)
        return LibraryItems.from_dict(resJson)

    def GetLibByName(self, libname):
        libs = self.GetAllLibs()
        lib = None
        for i in libs.Items:
            if(i.Name == libname):
                lib = i
                break
        return lib
