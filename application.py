import os, sys, json
import datetime
import copy
import uuid
import logging
from flask import Flask, request, jsonify 
from flask_cors import CORS
from pymongo import MongoClient
import skimage
import PIL

from analyzer import ResNet18
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
    if text is None:
        ret = {'failed' : 1, 'error' : 'No text field in json'}
        return jsonify(ret)
    
    date = datetime.datetime.now()
    doc_id = uuid.uuid4().hex
    db.docs.insert_one({"doc_id" : doc_id, 
                   "has_image" : False, 
                   "has_text" : True, 
                   "date_added" : date,
                   "date_updated" : date,
                   "text" : text})

    ret = {'failed' : 0, 'doc_id' : doc_id}
    return jsonify(ret)

@application.route('/find_duplicate', methods=['POST'])
def find_duplicate():
    data = request.get_json(force=True)
    text = data.get('text', None)
    image_url = data.get('image_url', None)
    if text is None and image_url is None:
        ret = {'failed' : 1, 'error' : 'No text or image_url found'}
        return jsonify(ret)

    duplicate_doc = db.docs.find_one({"text" : text})
    if duplicate_doc is None:
        ret = {'failed' : 0, 'duplicate' : 0}
    else:
        ret = {'failed' : 0, 'duplicate' : 1, 'doc_id' : duplicate_doc.get('doc_id')}

    return jsonify(ret)

@application.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json(force=True)
    image_url = data.get('image_url')
    if image_url is None:
        ret = {'failed' : 1, 'error' : 'No image_url found'}
    else:
        img = skimage.io.imread(image_url)
        img = PIL.Image.fromarray(img)
        embedding = get_image_embedding(img)
        ret = {'failed' : 0, 'embedding' : embedding.tolist()}

    return jsonify(ret)

def get_image_embedding(img):
    return resnet18.extract_feature(img)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
