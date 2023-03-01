from Classes.Calendar import Calendar
import json
from datetime import datetime, timedelta, timezone
from typing import List, Any
from dateutil.parser import isoparse

class FormulaFeature():

    #Calendar.GPs[0].Sessions[0].StartTime.st
    @staticmethod
    def FindClosestSession(data:Any):
        data = Calendar.from_dict(data)
        for x in data.GPs:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    return "Next session is: " + x.Name + " - " + y.Name + " @ " + y.StartTime.strftime("%d.%m.%Y %H:%M")
            


        
     


