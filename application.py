import os, sys, json, datetime, copy, uuid, requests
import logging
from flask import Flask, request, jsonify 
from flask_cors import CORS
from pymongo import MongoClient
from io import BytesIO
import skimage, PIL
import numpy as np

from analyzer import ResNet18, detect_text, image_from_url, detect_lang, doc2vec
from search import ImageSearch, TextSearch, DocSearch

imagesearch = ImageSearch()
docsearch = DocSearch()
textsearch = TextSearch()
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

    lang = detect_lang(text)
    vec = doc2vec(text)
    doc =  {
           "doc_id" : doc_id, 
           "has_image" : False, 
           "has_text" : True, 
           "date_added" : date,
           "date_updated" : date,
           "tags" : [],
           "text" : text,
           "lang" : lang,
           }
    if vec is not None:
        doc["vec"] = vec

    db.docs.insert_one(doc)
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
        image = image.convert('RGB') #take care of png(RGBA) issue
        vec = resnet18.extract_feature(image)
        doc_id, dist = imagesearch.search(vec)
        if doc_id is not None:
            ret = {'failed' : 0, 'duplicate' : 1, 'doc_id' : doc_id, 'distance' : dist}
        else:
            ret = {'failed' : 0, 'duplicate' : 0}

    elif text is not None:
        duplicate_doc = db.docs.find_one({"text" : text})
        vec = doc2vec(text)
        doc_id, dist = textsearch.search(vec)
        if duplicate_doc is not None:
            ret = {'failed' : 0, 'duplicate' : 1, 'doc_id' : duplicate_doc.get('doc_id')}
        elif doc_id is not None:
            ret = {'failed' : 0, 'duplicate' : 1, 'doc_id' : doc_id, 'distance': dist}
        else:
            ret = {'failed' : 0, 'duplicate' : 0}

    else:
        ret = {'failed' : 1, 'error' : 'something went wrong'}

    return jsonify(ret)

@application.route('/find_text', methods=['POST'])
def find_text():
    data = request.get_json(force=True)
    image_url = data.get('image_url')
    image_dict = image_from_url(image_url)
    return jsonify(detect_text(image_dict['image_bytes']))

@application.route('/delete_doc', methods=['POST'])
def delete_doc():
    data = request.get_json(force=True)
    doc_id = data.get('doc_id')
    ret = {}
    if not doc_id:
        ret['failed'] = 1
        ret['error'] = 'no doc id provided'
        return jsonify(ret)

    result = db.docs.delete_one({"doc_id" : doc_id})
    if result.deleted_count == 1:
        ret['failed'] = 0
    else:
        ret['failed'] = 1
        ret['error'] = 'no matching document'
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
        image = image.convert('RGB') #take care of png(RGBA) issue
        image_vec = resnet18.extract_feature(image)

        detected_text = detect_text(image_dict['image_bytes']).get('text','')
        lang = detect_lang(detected_text)

        #import ipdb; ipdb.set_trace()
        if detected_text == '' or None:
            text_vec = np.zeros(300).tolist()
            has_text = False
        else:
            text_vec = doc2vec(detected_text)
            has_text = True

        if lang is None:
            text_vec = np.zeros(300).tolist()
            has_text = True

        vec = np.hstack((image_vec, text_vec)).tolist()

        date = datetime.datetime.now()
        if doc_id is None:
            doc_id = uuid.uuid4().hex
        db.docs.insert_one({
                       "doc_id" : doc_id, 
                       "version": "1.1",
                       "has_image" : True, 
                       "has_text" : has_text, 
                       "text" : detected_text,
                       "tags" : [],
                       "date_added" : date,
                       "date_updated" : date,
                       "image_vec" : image_vec.tolist(),
                       "text_vec" : text_vec,
                       "vec" : vec,
                       })
        ret = {'doc_id': doc_id, 'failed' : 0}

        #update the search index
        imagesearch.update(doc_id, image_vec)
        docsearch.update(doc_id, vec)
        if has_text:
            textsearch.update(doc_id, text_vec)

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

def analyze_image(image_url):
    image = skimage.io.imread(image_url)
    image = PIL.Image.fromarray(image)
    embedding = get_image_embedding(image)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=7000)
