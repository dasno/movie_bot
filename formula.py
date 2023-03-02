from Classes.Calendar import Calendar, GrandPrix
from datetime import datetime, timedelta, timezone
from typing import Any
import pytz

class FormulaFeature():

    @staticmethod
    def FindClosestSession(data:Any):
        parsed = Calendar.from_dict(data)
        for x in parsed.GPs:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    return "Next session is: " + x.Name + " - " + y.Name + " @ " + y.StartTime.astimezone(pytz.timezone('Europe/Bratislava')).strftime("%d.%m.%Y %H:%M %Z")
            

    @staticmethod
    def GetAllGPs(data:Any):
        return Calendar.from_dict(data).GPs

        
     


