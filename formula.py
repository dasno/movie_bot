from Classes.Calendar import Calendar, GrandPrix, Session
from datetime import datetime, timedelta, timezone
from typing import Any, List
import pytz
import json
import requests
from Classes import Standings




class FormulaFeature():

    @staticmethod
    def FindClosestSession(data:Any, tzone):
        parsed = Calendar.from_dict(data)
        for x in parsed.GPs:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    res = FormulaFeature.GetFormattedSessionTime(y, tzone)
                    if res == "":
                        return "Incorrect timezone selected.\nTo see available timezones, go to: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\nUse canonical names"

                    return "Next session is: " + x.Name + " - " + y.Name + " @ " + FormulaFeature.GetFormattedSessionTime(y,tzone)

    @staticmethod
    def GetAllGPs(data:Any):
        return Calendar.from_dict(data).GPs
    
    def GetGP(data:Any, string:str):
        GPs = FormulaFeature.GetAllGPs(data)
        for x in GPs:
            if(x.Name == string):
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
        return stand.MRData.StandingsTable.StandingsLists[0].DriverStandings


        
     


