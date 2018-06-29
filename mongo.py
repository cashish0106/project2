# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.carDB

# Adding SUV manually to ensure script works everywhere
db.vehicle.insert_one(
    {
        'brand': ['acura','audi','bmw','infiniti','landrover','lexus','lincoln','mercedesbenz','porsche','volvo'],
        'model': ['mdx','q7','x5','qx60','range-rover','rx-350','mkx','m-class|gle-class','cayenne','xc90']
    }
)

db.years.inser_one(
    { 'year':[2014,2015,2016,2017,2018]
    }
)