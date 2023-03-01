from Classes.Calendar import Calendar
import json
from datetime import datetime, timedelta, timezone

jsonFile = open('f1times.json')

jsonDict = json.load(jsonFile)

