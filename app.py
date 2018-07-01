from flask import Flask, render_template
import pymongo
import csv

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.LuxSUVDB


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


@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
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

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)





            

        
    