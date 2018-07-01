import pymongo
import csv
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.LuxSUVDB

##Global variables


def isNumber(s):    
    try: 
        int(s)
        return True
    except ValueError:
        return False
def returnNumber(nmb,numtoreturn):
    try:
        int(nmb)
        return int(nmb)
    except ValueError:
        return numtoreturn
t="2014"
c=db[t].aggregate([{ 
  "$group": {
    "_id": "null", 
    "avg_price": { "$count": "$cash_price" } 
  } 
}])
for cx in c:
    print(cx)
def depreciation():
    collections = db.collection_names(include_system_collections=False)
    for collection in collections:
        #if(isNumber(collection)):
        #print(collection)
        if(isNumber(collection)):
            #print(collection)
            #if(int(collection)==2018):
                year=int(collection)
                header=["car","price"+str(year+1),"price"+str(year+2),"price"+str(year+3),"price"+str(year+4),"price"+str(year+5),"price5yeartotal","src"]
                cursor=db[collection].find({},{"brand":1,"model":1,"cash_price":1,"depreciation":1})
                with open(str(collection)+".csv", 'w') as outfile:
                    writer = csv.writer(outfile, lineterminator='\n')
                    writer.writerow(header)
                    for item in cursor:
                        car_detail=[]
                        car_detail.append(item["brand"].title()+item["model"].replace("-","").upper())
                        total_dep=0
                        for d in item["depreciation"]:
                            total_dep=total_dep+returnNumber(d,0)
                            dep= round(1 - ((returnNumber(item["cash_price"],0)-total_dep)/returnNumber(item["cash_price"],1)),2)
                            car_detail.append(dep)
                        car_detail.append("assets/data/"+item["brand"]+".png")
                        print(car_detail)
                        writer.writerow(car_detail)

            

        
    