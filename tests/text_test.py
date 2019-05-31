from pymongo import MongoClient
import uuid
import datetime
import os

mongo_url = os.environ['MONGO_URL']
cli = MongoClient(mongo_url)
db = cli.documents

with open("texts/19b727d3dea306a834906c785351127957257010.txt",'r') as f:
    data = f.read()

#date = datetime.datetime.now()
#db.docs.insert_one({"doc_id" : uuid.uuid4().hex, 
#               "has_image" : False, 
#               "has_text" : True, 
#               "date_added" : date,
#               "date_updated" : date,
#               "text" : data})

print(db.docs.find_one({"text" : data}))
