from datetime import datetime
from typing import List
from typing import Any
from datetime import datetime
from dateutil.parser import isoparse
from dataclasses import dataclass

@dataclass
class Session:
    Name :str
    StartTime:datetime
    
    @staticmethod
    def from_dict(obj: Any) -> 'Session':
        _Name = str(obj.get("name"))
        _StartTime = isoparse(obj.get("startTime"))
        return Session(_Name, _StartTime)
@dataclass
class GrandPrix:
    Round:str
    Name:str
    Map:str
    Sprint:bool
    Sessions:List[Session]

    @staticmethod
    def from_dict(obj:Any) -> 'GrandPrix':
        _Round = str(obj.get("round"))
        _Name = str(obj.get("name"))
        _Map = str(obj.get("map"))
        _Sprint = bool(obj.get("sprint"))
        _Sessions = [Session.from_dict(y) for y in obj.get("session")]
        return GrandPrix(_Round, _Name, _Map, _Sprint, _Sessions)
@dataclass
class Calendar:
    GPs:List[GrandPrix]

    @staticmethod
    def from_dict(obj:Any) -> 'Calendar':
        _GPs = [GrandPrix.from_dict(y) for y in obj.get("gp")]
        return Calendar(_GPs)

