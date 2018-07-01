import pymongo
import csv
#client = pymongo.MongoClient("mongodb+srv://admin:DsBs2018@cluster0-e19xd.mongodb.net:27017")
#client = pymongo.MongoClient("mongodb://admin:DsBs2018@mycluster0-shard-00-00.mongodb.net:27017,mycluster0-shard-00-01.mongodb.net:27017,mycluster0-shard-00-02.mongodb.net:27017/admin?ssl=true&replicaSet=Mycluster0-shard-0&authSource=admin")
client = pymongo.MongoClient("mongodb://admin:DsBs2018@Cluster0-shard-0/cluster0-shard-00-00-e19xd.mongodb.net:27017,cluster0-shard-00-01-e19xd.mongodb.net:27017,cluster0-shard-00-02-e19xd.mongodb.net:27017")

db = client.LuxSUVDB
collections = db.collection_names(include_system_collections=False)
for collection in collections:
    print(collection)