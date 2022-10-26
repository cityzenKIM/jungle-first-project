import certifi
ca=certifi.where()
from pymongo import MongoClient
client = MongoClient('mongodb+srv://tajunkim:wns41224--@cluster0.bxexa3c.mongodb.net/test', tlsCAFile=ca)
dblaundry = client.dblaundry

import uuid

Class = ['red', 'blue']
for c in range(2):
    for date in range(7):
        for time in range(7, 24):
            timeID = str(uuid.uuid4())
            dblaundry.reservations.insert_one({'class': Class[c],'timeID':timeID , 'date':date, 'time':time, 'name':False, 'userID':False})