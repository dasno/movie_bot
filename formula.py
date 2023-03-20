from Classes.Calendar import Calendar, GrandPrix, Session
from datetime import datetime, timedelta, timezone
from typing import Any, List
import pytz
import json
import requests
from Classes import Standings, Results

DEFAULT_TZONE = "Europe/Bratislava"


class FormulaFeature():

    @staticmethod
    def FindClosestSession(data:Any):
        parsed = FormulaFeature.GetAllGPs(data)
        for x in parsed:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    return x,y
    
    @staticmethod
    def GetAllGPs(data:Any) -> List[GrandPrix]:
        return Calendar.from_dict(data).GPs
    
    @staticmethod
    def FindClosestPastRace(data) -> GrandPrix:
        parsed = FormulaFeature.GetAllGPs(data)
        last:Any
        for x in parsed:
            if x.Sessions[4].StartTime + timedelta(minutes=180) > datetime.now(timezone.utc):
                return last
            last = x
    @staticmethod
    def GetGPByName(data:Any, string:str) -> GrandPrix:
        GPs = FormulaFeature.GetAllGPs(data)
        for x in GPs:
            if(x.Name == string):
                return x
    @staticmethod   
    def GetGPByRound(data:Any, round:int) -> GrandPrix:
        GPs = FormulaFeature.GetAllGPs(data)
        for x in GPs:
            if(x.Round == round):
                return x
            
    @staticmethod   
    def GetFormattedSessionTime(session:Session, tzone) -> str:
        if tzone == None or "":
            tzone = DEFAULT_TZONE

        try:
            return session.StartTime.astimezone(pytz.timezone(tzone)).strftime("%d.%m.%Y %H:%M %Z")
        except pytz.UnknownTimeZoneError:
            return None
    @staticmethod
    def GetStandings() -> List[Standings.DriverStanding]:
        response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
        stand = Standings.Root.from_dict(json.loads(response.content))
        return stand.MRData.StandingsTable
    
    @staticmethod
    def GetRaceStandingsByRound(round:int) -> Results.Race:
        response = requests.get("https://ergast.com/api/f1/current/{round}/results.json".format(round=str(round)))
        try:
            results = Results.Root.from_dict(json.loads(response.content))
        except TypeError:
            print("TypeError - GetRaceStandings - Querried round : {round}\n".format(round=round))
            return None
        try:
            return results.MRData.RaceTable.Races[0]
        except:
            return None
    @staticmethod
    def GetLatestResults(data):
        race = FormulaFeature.FindClosestPastRace(data)
        standings = FormulaFeature.GetRaceStandingsByRound(race.Round)
        return standings.Results
    
    @staticmethod
    def FormatResults(results:List[Results.Result]) -> str:
        response:str = ""
        for x in results:
                response += "\n{position}. {firstName} {lastName} - {points}".format(position=x.position, firstName=x.Driver.givenName, lastName=x.Driver.familyName, points=x.points)
        return response
    
    @staticmethod
    def IsOngoing(session:Session) -> bool:
        if session.Name == "Race":
            return session.StartTime + timedelta(minutes=160) < datetime.now()
        return session.StartTime + timedelta(minutes=60) < datetime.now()




        







        
     


