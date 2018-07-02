import pymongo
import csv
import os

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

if not os.path.exists("CSVFiles"):
    os.makedirs("CSVFiles")

collections = db.collection_names(include_system_collections=False)
for collection in collections:
    if(isNumber(collection)):
    #if(collection=="2018"):
        year=int(collection)
        cursor=db[collection].find({},{"brand":1,"model":1,"depreciation":1,"taxes":1,"financing":1,"fuel":1,"insurance":1,"maintenance":1,"repairs":1})
        for item in cursor:
            car_dict={}
            car_dict["header"]=["Year","depreciation","taxes","financing","fuel","insurance","maintenance","repairs"]
            for i in range(1,7):
                car_dict[str(year+i)]=[]
                car_dict[str(year+i)].append(year+i)
            filename = str(year)+item["brand"].title()+item["model"].replace("-","").upper()+".csv"
            d_year=year
            for d in item["depreciation"]:
                d_year+=1
                car_dict[str(d_year)].append(returnNumber(d,0))
            t_year=year
            for t in item["taxes"]:
                t_year+=1
                car_dict[str(t_year)].append(returnNumber(t,0))
            f_year=year
            for f in item["financing"]:
                f_year+=1
                car_dict[str(f_year)].append(returnNumber(f,0))
            fu_year=year
            for fu in item["fuel"]:
                fu_year+=1
                car_dict[str(fu_year)].append(returnNumber(fu,0))
            i_year=year
            for i in item["insurance"]:
                i_year+=1
                car_dict[str(i_year)].append(returnNumber(i,0))
            m_year=year
            for m in item["maintenance"]:
                m_year+=1
                car_dict[str(m_year)].append(returnNumber(m,0))
            r_year=year
            for r in item["repairs"]:
                r_year+=1
                car_dict[str(r_year)].append(returnNumber(r,0))
    
            with open("CSVFiles/"+filename, 'w') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                for key, value in car_dict.items():
                    writer.writerow(value)



def graph_scatter():
    collections = db.collection_names(include_system_collections=False)
    for collection in collections:
        if(isNumber(collection)):
            year=int(collection)
            header=["car","year","cash_price","true_cost"]
            cursor=db[collection].find({},{"brand":1,"model":1,"cash_price":1,"owning_cost":1})
            with open(str(collection)+"_scatter.csv", 'w') as outfile:
                writer = csv.writer(outfile, lineterminator='\n')
                writer.writerow(header)
                for item in cursor:
                    car_scatter=[]
                    car_scatter.append(item["brand"].title()+item["model"].replace("-","").upper())
                    car_scatter.append(year)
                    car_scatter.append(item["cash_price"])
                    car_scatter.append(item["owning_cost"])
                    writer.writerow(car_scatter)
                


def line_char():
    collections = db.collection_names(include_system_collections=False)
    for collection in collections:
        if(isNumber(collection)):
            year=int(collection)
            line_dict={}
            line_dict["header"]=["Year"]
            line_dict[str(year)]=[]
            line_dict[str(year)].append(year)
            for i in range(1,7):
            # print(year+i)
                line_dict[str(year+i)]=[]
                line_dict[str(year+i)].append(year+i)
            cursor=db[collection].find({},{"brand":1,"model":1,"cash_price":1,"depreciation":1})
            for item in cursor:
                line_dict["header"].append(item["brand"].title()+item["model"].replace("-","").upper())
                
                line_dict[str(year)].append((returnNumber(item["cash_price"],0)))
                total_dep=0
                dep_year=year
                for d in item["depreciation"]:
                    total_dep=total_dep+returnNumber(d,0)
                    dep_year=dep_year+1
                    dep= returnNumber(item["cash_price"],0)-total_dep
                    line_dict[str(dep_year)].append(dep)
            
            with open(str(collection)+'_line.csv', 'w') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in line_dict.items():
                    writer.writerow(value)
            #print(line_dict)


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

            

        
    