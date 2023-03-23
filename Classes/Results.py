from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class AverageSpeed:
    units: str
    speed: str

    @staticmethod
    def from_dict(obj: Any) -> 'AverageSpeed':
        _units = str(obj.get("units"))
        _speed = str(obj.get("speed"))
        return AverageSpeed(_units, _speed)



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
class Time:
    millis: str
    time: str

    @staticmethod
    def from_dict(obj: Any) -> 'Time':
        _millis = str(obj.get("millis"))
        _time = str(obj.get("time"))
        return Time(_millis, _time)

@dataclass
class FastestLap:
    rank: str
    lap: str
    Time: Time
    AverageSpeed: AverageSpeed

    @staticmethod
    def from_dict(obj: Any) -> 'FastestLap':
        _rank = str(obj.get("rank"))
        _lap = str(obj.get("lap"))
        _Time = Time.from_dict(obj.get("Time"))
        _AverageSpeed = AverageSpeed.from_dict(obj.get("AverageSpeed"))
        return FastestLap(_rank, _lap, _Time, _AverageSpeed)

@dataclass
class Location:
    lat: str
    long: str
    locality: str
    country: str

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        _lat = str(obj.get("lat"))
        _long = str(obj.get("long"))
        _locality = str(obj.get("locality"))
        _country = str(obj.get("country"))
        return Location(_lat, _long, _locality, _country)
    
    
@dataclass
class Circuit:
    circuitId: str
    url: str
    circuitName: str
    Location: Location

    @staticmethod
    def from_dict(obj: Any) -> 'Circuit':
        _circuitId = str(obj.get("circuitId"))
        _url = str(obj.get("url"))
        _circuitName = str(obj.get("circuitName"))
        _Location = Location.from_dict(obj.get("Location"))
        return Circuit(_circuitId, _url, _circuitName, _Location)
    
@dataclass
class Result:
    number: str
    position: str
    positionText: str
    points: str
    Driver: Driver
    Constructor: Constructor
    grid: str
    laps: str
    status: str
    Time: Time
    FastestLap: FastestLap

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        _number = str(obj.get("number"))
        _position = str(obj.get("position"))
        _positionText = str(obj.get("positionText"))
        _points = str(obj.get("points"))
        _Driver = Driver.from_dict(obj.get("Driver"))
        _Constructor = Constructor.from_dict(obj.get("Constructor"))
        _grid = str(obj.get("grid"))
        _laps = str(obj.get("laps"))
        _status = str(obj.get("status"))
        if obj.get("Time") is None:
            _Time = Time(None, None)
        else:
            _Time = Time.from_dict(obj.get("Time"))
        try:
            _FastestLap = FastestLap.from_dict(obj.get("FastestLap"))
        except AttributeError:
            _FastestLap = None
        return Result(_number, _position, _positionText, _points, _Driver, _Constructor, _grid, _laps, _status, _Time, _FastestLap)

@dataclass
class Race:
    season: str
    round: str
    url: str
    raceName: str
    Circuit: Circuit
    date: str
    time: str
    Results: List[Result]

    @staticmethod
    def from_dict(obj: Any) -> 'Race':
        _season = str(obj.get("season"))
        _round = str(obj.get("round"))
        _url = str(obj.get("url"))
        _raceName = str(obj.get("raceName"))
        _Circuit = Circuit.from_dict(obj.get("Circuit"))
        _date = str(obj.get("date"))
        _time = str(obj.get("time"))
        _Results = [Result.from_dict(y) for y in obj.get("Results")]
        return Race(_season, _round, _url, _raceName, _Circuit, _date, _time, _Results)

@dataclass
class RaceTable:
    season: str
    round: str
    Races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'RaceTable':
        _season = str(obj.get("season"))
        _round = str(obj.get("round"))
        _Races = [Race.from_dict(y) for y in obj.get("Races")]
        return RaceTable(_season, _round, _Races)
    

@dataclass
class MRData:
    xmlns: str
    series: str
    url: str
    limit: str
    offset: str
    total: str
    RaceTable: RaceTable

    @staticmethod
    def from_dict(obj: Any) -> 'MRData':
        _xmlns = str(obj.get("xmlns"))
        _series = str(obj.get("series"))
        _url = str(obj.get("url"))
        _limit = str(obj.get("limit"))
        _offset = str(obj.get("offset"))
        _total = str(obj.get("total"))
        _RaceTable = RaceTable.from_dict(obj.get("RaceTable"))
        return MRData(_xmlns, _series, _url, _limit, _offset, _total, _RaceTable)

@dataclass
class Root:
    MRData: MRData

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _MRData = MRData.from_dict(obj.get("MRData"))
        return Root(_MRData)