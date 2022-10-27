import certifi
ca=certifi.where()
from pymongo import MongoClient
client = MongoClient('mongodb://ajm0718:qhemzk0204@15.165.248.49', 27017)
dblaundry = client.dblaundry

import uuid

dblaundry.thisweekday.insert_one({'weekday':2, 'week': 'day'})

Class = ['red', 'blue']
for c in range(2):
    for date in range(7):
        for time in range(7, 24):
            timeID = str(uuid.uuid4())
            dblaundry.reservations.insert_one({'class': Class[c],'timeID':timeID , 'date':date, 'time':time, 'name':False, 'userID':False})