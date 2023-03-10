from Classes.Calendar import Calendar, GrandPrix, Session
from datetime import datetime, timedelta, timezone
from typing import Any, List
import pytz
import json
import requests
from Classes import Standings, Results




class FormulaFeature():

    @staticmethod
    def FindClosestSession(data:Any, tzone):
        parsed = FormulaFeature.GetAllGPs(data)
        for x in parsed:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    res = FormulaFeature.GetFormattedSessionTime(y, tzone)
                    if res == "":
                        return "Incorrect timezone selected.\nTo see available timezones, go to: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\nUse canonical names"

                    return "Next session is: " + x.Name + " - " + y.Name + " @ " + FormulaFeature.GetFormattedSessionTime(y,tzone)
    
    


    @staticmethod
    def GetAllGPs(data:Any) -> List[GrandPrix]:
        return Calendar.from_dict(data).GPs
    
    def FindClosestPastRace(data) -> GrandPrix:
        parsed = FormulaFeature.GetAllGPs(data)
        last:Any
        for x in parsed:
            if x.Sessions[4].StartTime + timedelta(minutes=180) > datetime.now(timezone.utc):
                return last
            last = x
    
    def GetGPByName(data:Any, string:str) -> GrandPrix:
        GPs = FormulaFeature.GetAllGPs(data)
        for x in GPs:
            if(x.Name == string):
                return x
        
    def GetGPByRound(data:Any, round:int) -> GrandPrix:
        GPs = FormulaFeature.GetAllGPs(data)
        for x in GPs:
            if(x.Round == round):
                return x
            
        
    def GetFormattedSessionTime(session:Session, tzone) -> str:
        print("Selected timezone: {tzone}".format(tzone=tzone))
        if tzone == None or "":
            tzone = 'Europe/Bratislava'

        try:
            return session.StartTime.astimezone(pytz.timezone(tzone)).strftime("%d.%m.%Y %H:%M %Z")
        except pytz.UnknownTimeZoneError:
            return ""
    
    def GetStandings() -> List[Standings.DriverStanding]:
        response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
        stand = Standings.Root.from_dict(json.loads(response.content))
        return stand.MRData.StandingsTable
    
    def GetRaceStandingsByRound(round:int) -> Results.Race:
        response = requests.get("https://ergast.com/api/f1/current/{round}/results.json".format(round=round))
        try:
            results = Results.Root.from_dict(json.loads(response.content))
        except TypeError:
            print("TypeError - GetRaceStandings - Querried round : {round}\n{content}".format(round=round, content=response.content))
            return None
        try:
            return results.MRData.RaceTable.Races[0]
        except IndexError:
            return None
    
    def GetLatestResults(data):
        race = FormulaFeature.FindClosestPastRace(data)
        standings = FormulaFeature.GetRaceStandingsByRound(race.Round)



        







        
     


