import os, sys, json, datetime, copy, uuid, requests
import logging
from flask import Flask, request, jsonify 
from flask_cors import CORS
from pymongo import MongoClient
from io import BytesIO
import skimage, PIL
import numpy as np

from analyzer import ResNet18, detect_text
from search import ImageSearch

imagesearch = ImageSearch()
resnet18 = ResNet18()

application = Flask(__name__)
CORS(application)

logger = logging.getLogger("tattle-api")

mongo_url = os.environ['MONGO_URL']
cli = MongoClient(mongo_url)
db = cli.documents

@application.route('/health')
def health_check():
    logger.debug('<health-check>')
    return "OK"

@application.route('/upload_text', methods=['POST'])
def upload_text():
    data = request.get_json(force=True)
    text = data.get('text',None)
    doc_id = data.get('doc_id',None)
    if text is None:
        ret = {'failed' : 1, 'error' : 'No text field in json'}
        return jsonify(ret)
    
    date = datetime.datetime.now()
    if doc_id is None:
        doc_id = uuid.uuid4().hex
    db.docs.insert_one({
                   "doc_id" : doc_id, 
                   "has_image" : False, 
                   "has_text" : True, 
                   "date_added" : date,
                   "date_updated" : date,
                   "tags" : [],
                   "text" : text
                   })

    ret = {'failed' : 0, 'doc_id' : doc_id}
    return jsonify(ret)

@application.route('/find_duplicate', methods=['POST'])
def find_duplicate():
    data = request.get_json(force=True)
    text = data.get('text', None)
    image_url = data.get('image_url', None)
    if text is None and image_url is None:
        ret = {'failed' : 1, 'error' : 'No text or image_url found'}

    elif image_url is not None:
        image_dict = image_from_url(image_url)
        image = image_dict['image']
        vec = resnet18.extract_feature(image)
        doc_id, dist = imagesearch.search(vec)
        if doc_id is not None:
            ret = {'failed' : 0, 'duplicate' : True, 'doc_id' : doc_id, 'distance' : dist}
        else:
            ret = {'failed' : 0, 'duplicate' : False}

    elif text is not None:
        duplicate_doc = db.docs.find_one({"text" : text})
        if duplicate_doc is None:
            ret = {'failed' : 0, 'duplicate' : 0}
        else:
            ret = {'failed' : 0, 'duplicate' : 1, 'doc_id' : duplicate_doc.get('doc_id')}

    else:
        ret = {'failed' : 1, 'error' : 'something went wrong'}

    return jsonify(ret)

@application.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json(force=True)
    image_url = data.get('image_url')
    doc_id = data.get('doc_id',None)
    if image_url is None:
        ret = {'failed' : 1, 'error' : 'No image_url found'}
    else:
        image_dict = image_from_url(image_url)
        image = image_dict['image']
        vec = resnet18.extract_feature(image)
        #detected_text = detect_text(image_dict['image_bytes'])

        date = datetime.datetime.now()
        if doc_id is None:
            doc_id = uuid.uuid4().hex
        db.docs.insert_one({
                       "doc_id" : doc_id, 
                       "has_image" : True, 
                       "has_text" : False, 
                       "tags" : [],
                       "date_added" : date,
                       "date_updated" : date,
                       "fingerprint" : vec.tolist(),
                       })
        ret = {'doc_id': doc_id, 'failed' : 0}

        #update the search index
        imagesearch.update(doc_id, vec)

    return jsonify(ret)

@application.route('/update_tags', methods=['POST'])
def update_tags():
    data = request.get_json(force=True)
    doc_id = data.get('doc_id')
    tags = data.get('tags')
    if doc_id is None:
        ret = {'failed' : 1, 'error' : 'no doc_id provided'}
    elif tags is None:
        ret = {'failed' : 1, 'error' : 'no tags provided'}
    else:
        doc = db.docs.find_one({"doc_id" : doc_id})
        if doc is None:
            ret = {'failed' : 1, 'error' : 'doc not found'}
        else:
            updated_tags = list(set(doc.get('tags',[]) + tags))
            date = datetime.datetime.now()
            db.docs.update_one({"doc_id" : doc_id}, {"$set" : 
                {"tags" : updated_tags, "date_updated" : date}})
            ret = {'failed' : 0}
    return jsonify(ret)

def image_from_url(image_url):
    resp = requests.get(image_url)
    image_bytes = resp.content
    image = PIL.Image.open(BytesIO(image_bytes))
    image_array = np.array(image)
    return {'image' : image, 'image_array' : image_array, 'image_bytes' : image_bytes}

def analyze_image(image_url):
    image = skimage.io.imread(image_url)
    image = PIL.Image.fromarray(image)
    embedding = get_image_embedding(image)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=7000)
