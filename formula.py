from Classes.Calendar import Calendar, GrandPrix, Session
from datetime import datetime, timedelta, timezone
from typing import Any, List
import pytz
import json
import requests
from Classes import Standings





class FormulaFeature():

    @staticmethod
    def FindClosestSession(data:Any):
        parsed = Calendar.from_dict(data)
        for x in parsed.GPs:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    return "Next session is: " + x.Name + " - " + y.Name + " @ " + FormulaFeature.GetFormattedSessionTime(y)

    @staticmethod
    def GetAllGPs(data:Any):
        return Calendar.from_dict(data).GPs
    
    def GetGP(data:Any, string:str):
        GPs = FormulaFeature.GetAllGPs(data)
        for x in GPs:
            if(x.Name == string):
                return x
            
        
    def GetFormattedSessionTime(session:Session) -> str:
        return session.StartTime.astimezone(pytz.timezone('Europe/Bratislava')).strftime("%d.%m.%Y %H:%M %Z")
    
    def GetStandings() -> List[Standings.DriverStanding]:
        response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
        stand = Standings.Root.from_dict(json.loads(response.content))
        return stand.MRData.StandingsTable.StandingsLists[0].DriverStandings


        
     


