import os
import sys
import json
import datetime
import copy
import uuid
import requests
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
# from pymongo import MongoClient
from io import BytesIO
import skimage
import PIL
import numpy as np
from os import listdir

from analyzer import ResNet18, detect_text, image_from_url, detect_lang, doc2vec
from search import ImageSearch, DocSearch
from db import sqlDatabase, mongoDB, default_db_doc

# TODO: write unittests!!!

db_type = 'mongo'
db_filename = 'docs_sqlite_db.db'
imagesearch = ImageSearch(db_type=db_type, db_filename=db_filename)
docsearch = DocSearch(db_type=db_type, db_filename=db_filename)
resnet18 = ResNet18()

application = Flask(__name__)
CORS(application)

logger = logging.getLogger("tattle-api")

"""
MongoDB schema: {
    "doc_id" : doc_id,
    "has_image" : False,
    "has_text" : True,
    "date_added" : date,
    "date_updated" : date,
    "tags" : [],
    "text" : text,
    "lang" : lang,
    "vec": vec
}
SQLite schema: {
    "doc_id: doc_id,
    "has_image" : False,
    "has_text" : True,
    "date_added" : date,
    "date_updated" : date,
    "tags" : [],
    "textdata" : text,
    "vec": word2vec,
    "lang" : lang,
    "imagedata": image bytes,
    "imagemetadata": image mode/size,
    "imagevec": embedding
}
"""
if db_type == 'mongo':
    db = mongoDB()
    docs = db.docs


@application.route('/health')
def health_check():
    """
    what does this do?
    """
    logger.debug('<health-check>')
    return "OK"


@application.route('/upload_text', methods=['POST'])
def upload_text():
    """
    uploads text to mongodb
    input: json with keys {'doc_id', 'image_url', 'text'}
    """
    data = request.get_json(force=True)
    text = data.get('text', None)

    doc_id = data.get('doc_id', None)  # why would they give an id?
    if text is None:
        ret = {'failed': 1, 'error': 'No text field in json'}
        return jsonify(ret)

    if db_type == 'mongo':
        date = datetime.datetime.now()
        if doc_id is None:
            doc_id = uuid.uuid4().hex
    elif db_type == 'sqlite':
        date = datetime.date.today()
        doc_id = None

    textvec, lang = doc2vec(text)
    doc = default_db_doc(doc_id=doc_id, has_text=True, text=text, lang=lang)
    if textvec is not None:
        doc["text_vec"] = textvec.tolist()

    if db_type == 'mongo':
        docs.insert_one(doc)
    elif db_type == 'sqlite':
        with sqlDatabase(db_filename) as db:
            db.execute(
                "INSERT into documents(has_image, has_text, date_added, date_updated, textdata, lang, vec) values(?,?,?,?,?,?,?)", (0, 1, date, date, text, lang, textvec))
    ret = {'failed': 0, 'doc_id': doc_id}
    return jsonify(ret)


@application.route('/find_duplicate', methods=['POST'])
def find_duplicate():
    # force=true: ignore mimetype (media type) https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
    data = request.get_json(force=True)
    text = data.get('text', None)
    image_url = data.get('image_url', None)
    if text is None and image_url is None:
        ret = {'failed': 1, 'error': 'No text or image_url found'}

    elif image_url is not None:
        image_dict = image_from_url(image_url)
        image = image_dict['image']
        vec = resnet18.extract_feature(image)
        doc_id, dist = imagesearch.search(vec)
        if doc_id is not None:
            ret = {'failed': 0, 'duplicate': 1,
                   'doc_id': doc_id, 'distance': dist}
        else:
            ret = {'failed': 0, 'duplicate': 0}

    elif text is not None:
        if db_type == 'mongo':

            duplicate_doc = docs.find_one({"text": text})
            # *is this just an exact match?
        elif db_type == 'sqlite':
            with sqlDatabase(db_filename) as db:
                temp = db.query(
                    'SELECT doc_id, textdata from documents where textdata=?', [text])
            if len(temp) == 0:
                duplicate_doc = None
            else:
                duplicate_doc = {
                    'doc_id': temp[0][0], 'textdata': temp[0][1]}

        textvec, _ = doc2vec(text)
        if _ == None:
            return jsonify({'failed': 1, 'error': textvec})

        doc_id, dist = docsearch.search(textvec.tolist())
        if duplicate_doc is not None:
            ret = {'failed': 0, 'duplicate': 1,
                   'doc_id': duplicate_doc.get('doc_id')}
        elif doc_id is not None:
            ret = {'failed': 0, 'duplicate': 1,
                   'doc_id': doc_id, 'distance': dist}
        else:
            ret = {'failed': 0, 'duplicate': 0}

    else:
        ret = {'failed': 1, 'error': 'something went wrong'}

    return jsonify(ret)


@application.route('/find_text', methods=['POST'])
def find_text():
    data = request.get_json(force=True)
    image_url = data.get('image_url')
    image_dict = image_from_url(image_url)
    return jsonify(detect_text(image_dict['image_bytes']))


@application.route('/upload_image', methods=['POST'])
def upload_image():
    """
    uploads image to mongodb, sqlite
    input: json with keys {'doc_id', 'image_url', 'text'}
    """
    data = request.get_json(force=True)
    image_url = data.get('image_url')
    doc_id = data.get('doc_id', None)  # why would they give an id?
    if image_url is None:
        ret = {'failed': 1, 'error': 'No image_url found'}
    else:
        image_dict = image_from_url(image_url)
        image = image_dict['image']
        image = image.convert('RGB')  # take care of png(RGBA) issue
        image_vec = resnet18.extract_feature(image)
        # detected_text = detect_text(image_dict['image_bytes'])

    if db_type == 'mongo':
        date = datetime.datetime.now()
        if doc_id is None:
            doc_id = uuid.uuid4().hex
        doc = default_db_doc(doc_id=doc_id, has_image=True,
                             image_vec=image_vec.tolist())
        docs.insert_one(doc)

        ret = {'doc_id': doc_id, 'failed': 0}
    elif db_type == 'sqlite':
        date = datetime.date.today()
        doc_id = None
        imagedata = image.tobytes()
        imagemetadata = str({'mode': image.mode, 'size': image.size})
        imagevec = image_vec

        with sqlDatabase(db_filename) as db:
            doc_id = db.query("SELECT COUNT(doc_id) from documents")
            db.execute(
                "INSERT into documents(has_image, has_text, date_added, date_updated, imagedata, imagemetadata, imagevec) values(?,?,?,?,?,?,?)", (1, 0, date, date, imagedata, imagemetadata, imagevec))

        # update the search index
        imagesearch.update(doc_id, image_vec)

    return jsonify(ret)


@application.route('/update_tags', methods=['POST'])
def update_tags():
    """
    uploads tags related to a doc_id to mongodb
    input: json with keys {'doc_id', 'tags'}
    """
    data = request.get_json(force=True)
    doc_id = data.get('doc_id')
    tags = data.get('tags')
    if doc_id is None:
        ret = {'failed': 1, 'error': 'no doc_id provided'}
    elif tags is None:
        ret = {'failed': 1, 'error': 'no tags provided'}
    else:
        doc = docs.find_one({"doc_id": doc_id})
        if doc is None:
            ret = {'failed': 1, 'error': 'doc not found'}
        else:
            updated_tags = list(set(doc.get('tags', []) + tags))
            date = datetime.datetime.now()
            docs.update_one({"doc_id": doc_id}, {"$set":
                                                 {"tags": updated_tags, "date_updated": date}})
            ret = {'failed': 0}
    return jsonify(ret)


if __name__ == "__main__":
    # application would not with 'x' permissions
    # chmod 644 application.py
    application.run(debug=True)
    # application.run(host="0.0.0.0", port=7000)
