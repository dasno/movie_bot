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
class ConstructorStanding:
    position: str
    positionText: str
    points: str
    wins: str
    Constructor: Constructor

    @staticmethod
    def from_dict(obj: Any) -> 'ConstructorStanding':
        _position = str(obj.get("position"))
        _positionText = str(obj.get("positionText"))
        _points = str(obj.get("points"))
        _wins = str(obj.get("wins"))
        _Constructor = Constructor.from_dict(obj.get("Constructor"))
        return ConstructorStanding(_position, _positionText, _points, _wins, _Constructor)



@dataclass
class StandingsList:
    season: str
    round: str
    ConstructorStandings: List[ConstructorStanding]

    @staticmethod
    def from_dict(obj: Any) -> 'StandingsList':
        _season = str(obj.get("season"))
        _round = str(obj.get("round"))
        _ConstructorStandings = [ConstructorStanding.from_dict(y) for y in obj.get("ConstructorStandings")]
        return StandingsList(_season, _round, _ConstructorStandings)

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