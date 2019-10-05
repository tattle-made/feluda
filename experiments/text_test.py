from pymongo import MongoClient
import uuid
import datetime
import os
import urllib.request

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

def mime_type(url):
    with urllib.request.urlopen(url) as response:
        info = response.info()
        print(info.get_content_type())      # -> text/html?
        print(info.get_content_maintype())  # -> text?
        print(info.get_content_subtype())   # -> html?

if __name__ == "__main__":
    url1 = "https://firebasestorage.googleapis.com/v0/b/crowdsourcesocialposts.appspot.com/o/text-posts%2F079c92f5-a4cb-4f92-a2ad-72a9da9545bf?alt=media&token=cb986540-f302-4cb4-91b3-1ead32627fbf"
    url2 = "https://firebasestorage.googleapis.com/v0/b/crowdsourcesocialposts.appspot.com/o/image-posts%2F06c1eaa0-feea-42e5-8eee-b3ab3b099831?alt=media&token=cf1b9b4f-fa1f-48e4-8d64-82476cfeec1a"
    mime_type(url1)
    mime_type(url2)
