from ast import keyword
from sqlite3 import connect
from xml.etree.ElementTree import tostring
from Classes.Connection import Connection
from Classes.AllLibs import AllLibs
from Classes.LibraryItems import LibraryItems
import json
import requests


class Jellyapi:
    
    def __init__(self, jelly_address, jelly_api, jelly_uid):
        self.API_KEY = jelly_api
        self.ADDRESS = jelly_address
        self.JELLY_UID = jelly_uid
        self.con = Connection(self.API_KEY, self.ADDRESS)


    def get_all_libs(self):
        header = {'X-Emby-Token':self.API_KEY}
        target = self.con.Address + "/Items"
        response = requests.get(target,
                                headers=header,
                                params={'userId':self.JELLY_UID})
        response_json = json.loads(response.content)
        return AllLibs.from_dict(response_json)

    def get_library_items(self, libId):
        header = {'X-Emby-Token':self.API_KEY}
        target = self.con.Address + "/Items"
        response = requests.get(target,
                                headers=header,
                                params= {'userId':self.JELLY_UID,
                                        'parentId' : libId})
        response_json = json.loads(response.content)
        return LibraryItems.from_dict(response_json)

    def get_lib_by_name(self, libname):
        libs = self.get_all_libs()
        lib = None
        for i in libs.Items:
            if(i.name == libname):
                lib = i
                break
        return lib
