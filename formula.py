from Classes.Calendar import Calendar, GrandPrix, Session
from datetime import datetime, timedelta, timezone
from typing import Any, List
import pytz
import json
import requests
from Classes import DriverStandings, Results, ConstructorStandings

DEFAULT_TZONE = "Europe/Bratislava"
DRIVER_STANDINGS_URL = 'http://ergast.com/api/f1/current/driverStandings.json'
CONSTRUCTOR_STANDINGS_URL = 'https://ergast.com/api/f1/current/constructorStandings.json'
RACE_RESULTS_URL = "https://ergast.com/api/f1/current/{round}/results.json"


class FormulaFeature():

    @staticmethod
    def find_closest_session(data:Any):
        parsed = FormulaFeature.get_all_gps(data)
        for x in parsed:
            for y in x.Sessions:
                if (y.StartTime) >= datetime.now(timezone.utc):
                    return x,y
    
    @staticmethod
    def get_all_gps(data:Any) -> List[GrandPrix]:
        return Calendar.from_dict(data).GPs
    
    @staticmethod
    def find_closest_past_race(data) -> GrandPrix:
        parsed = FormulaFeature.get_all_gps(data)
        last:Any
        for x in parsed:
            if x.Sessions[4].StartTime + timedelta(minutes=180) > datetime.now(timezone.utc):
                return last
            last = x
    @staticmethod
    def get_gp_by_name(data:Any, string:str) -> GrandPrix:
        gp_list = FormulaFeature.get_all_gps(data)
        for x in gp_list:
            if(x.Name == string):
                return x
    @staticmethod   
    def get_gp_by_round(data:Any, round:int) -> GrandPrix:
        gp_list = FormulaFeature.get_all_gps(data)
        for x in gp_list:
            if(x.Round == round):
                return x
            
    @staticmethod   
    def get_formatted_session_time(session:Session, tzone) -> str:
        if tzone == None or "":
            tzone = DEFAULT_TZONE

        try:
            return session.StartTime.astimezone(pytz.timezone(tzone)).strftime("%d.%m.%Y %H:%M %Z")
        except pytz.UnknownTimeZoneError:
            return None
    @staticmethod
    def get_driver_standings() -> List[DriverStandings.DriverStanding]:
        response = requests.get(DRIVER_STANDINGS_URL)
        stand = DriverStandings.Root.from_dict(json.loads(response.content))
        return stand.MRData.StandingsTable
    
    @staticmethod
    def get_race_results_by_round(round:int) -> Results.Race:
        response = requests.get(RACE_RESULTS_URL.format(round=str(round)))
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
    def get_latest_results(data):
        race = FormulaFeature.find_closest_past_race(data)
        standings = FormulaFeature.get_race_results_by_round(race.Round)
        return standings.Results
    
    @staticmethod
    def format_results(results:List[Results.Result]) -> str:
        response:str = ""
        for x in results:
            if x.position == "1":
                position=":first_place:"
            elif x.position == "2":
                position=":second_place:"
            elif x.position == "3":
                position=":third_place:"
            else:
                position = x.position+"."
            
            if x.FastestLap == None:
                fl = ""
                points = x.points
            
            elif x.FastestLap.rank == "1" and int(x.position) <= 10:
                print(x.FastestLap.rank)
                fl = ":stopwatch:"
                points = x.points
                #TODO: return to this when api data is corrected.

            elif x.FastestLap.rank == "1" and int(x.position) > 10:
                fl = ":stopwatch:"
                points = x.points
            else:
                fl = ""
                points = x.points
            
            if x.Time.time == None:
                if x.positionText == "R":
                    time = "DNF"
                else:
                    time = x.status
            else:
                time = x.Time.time
                
            response += "\n{position}\t{firstName} {lastName} {fl}  {time}  - {points}".format(position=position,
                                                                                    firstName=x.Driver.givenName,
                                                                                    lastName=x.Driver.familyName,
                                                                                    points=points,
                                                                                    time=time,
                                                                                    fl=fl)
        return response
    
    @staticmethod #untested
    def is_ongoing(session:Session) -> bool:
        if session.Name == "Race":
            return session.StartTime + timedelta(minutes=160) < datetime.now(timezone.utc)
        return (session.StartTime + timedelta(minutes=60)) < datetime.now(timezone.utc)
    
    @staticmethod
    def get_constructor_standings() -> List[ConstructorStandings.ConstructorStanding]:
        response = requests.get(CONSTRUCTOR_STANDINGS_URL)
        stand = ConstructorStandings.Root.from_dict(json.loads(response.content))
        return stand.MRData.StandingsTable




        







        
     


