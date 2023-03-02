from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Constructor:
    constructorId: str
    url: str
    name: str
    nationality: str

    @staticmethod
    def from_dict(obj: Any) -> 'Constructor':
        _constructorId = str(obj.get("constructorId"))
        _url = str(obj.get("url"))
        _name = str(obj.get("name"))
        _nationality = str(obj.get("nationality"))
        return Constructor(_constructorId, _url, _name, _nationality)

@dataclass
class Driver:
    driverId: str
    permanentNumber: str
    code: str
    url: str
    givenName: str
    familyName: str
    dateOfBirth: str
    nationality: str

    @staticmethod
    def from_dict(obj: Any) -> 'Driver':
        _driverId = str(obj.get("driverId"))
        _permanentNumber = str(obj.get("permanentNumber"))
        _code = str(obj.get("code"))
        _url = str(obj.get("url"))
        _givenName = str(obj.get("givenName"))
        _familyName = str(obj.get("familyName"))
        _dateOfBirth = str(obj.get("dateOfBirth"))
        _nationality = str(obj.get("nationality"))
        return Driver(_driverId, _permanentNumber, _code, _url, _givenName, _familyName, _dateOfBirth, _nationality)

@dataclass
class DriverStanding:
    position: str
    positionText: str
    points: str
    wins: str
    Driver: Driver
    Constructors: List[Constructor]

    @staticmethod
    def from_dict(obj: Any) -> 'DriverStanding':
        _position = str(obj.get("position"))
        _positionText = str(obj.get("positionText"))
        _points = str(obj.get("points"))
        _wins = str(obj.get("wins"))
        _Driver = Driver.from_dict(obj.get("Driver"))
        _Constructors = [Constructor.from_dict(y) for y in obj.get("Constructors")]
        return DriverStanding(_position, _positionText, _points, _wins, _Driver, _Constructors)
    
@dataclass
class StandingsList:
    season: str
    round: str
    DriverStandings: List[DriverStanding]

    @staticmethod
    def from_dict(obj: Any) -> 'StandingsList':
        _season = str(obj.get("season"))
        _round = str(obj.get("round"))
        _DriverStandings = [DriverStanding.from_dict(y) for y in obj.get("DriverStandings")]
        return StandingsList(_season, _round, _DriverStandings)

@dataclass
class StandingsTable:
    season: str
    StandingsLists: List[StandingsList]

    @staticmethod
    def from_dict(obj: Any) -> 'StandingsTable':
        _season = str(obj.get("season"))
        _StandingsLists = [StandingsList.from_dict(y) for y in obj.get("StandingsLists")]
        return StandingsTable(_season, _StandingsLists)

@dataclass
class MRData:
    xmlns: str
    series: str
    url: str
    limit: str
    offset: str
    total: str
    StandingsTable: StandingsTable

    @staticmethod
    def from_dict(obj: Any) -> 'MRData':
        _xmlns = str(obj.get("xmlns"))
        _series = str(obj.get("series"))
        _url = str(obj.get("url"))
        _limit = str(obj.get("limit"))
        _offset = str(obj.get("offset"))
        _total = str(obj.get("total"))
        _StandingsTable = StandingsTable.from_dict(obj.get("StandingsTable"))
        return MRData(_xmlns, _series, _url, _limit, _offset, _total, _StandingsTable)

@dataclass
class Root:
    MRData: MRData

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _MRData = MRData.from_dict(obj.get("MRData"))
        return Root(_MRData)



# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
