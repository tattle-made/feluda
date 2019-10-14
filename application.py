from search import DocSearch, ImageSearch, TextSearch
from flask_cors import CORS
from db import default_db_doc, mongoDB, sqlDatabase
import datetime
import logging
from os import environ

from flask import Flask, jsonify, render_template, request

from analyzer import ResNet18, detect_text, doc2vec, image_from_url

db_type = 'mongo'
db_filename = 'docs_sqlite_db.db'
# !DEFINE THRESHOLDS HERE
imagesearch = ImageSearch(db_type=db_type, db_filename=db_filename, threshold=10)
textsearch = TextSearch(db_type=db_type, db_filename=db_filename ,threshold=0.6)
docsearch = DocSearch(db_type=db_type, db_filename=db_filename, threshold=20)
resnet18 = ResNet18()

application = Flask(__name__)
CORS(application)

# ?
logger = logging.getLogger("tattle-api")

"""
MongoDB schema: {
    "doc_id": doc_id,
    "has_image": has_image,
    "has_text": has_text,
    "date_added": date_added,
    "date_updated": date_updated,
    "tags": tags,
    "text": text,
    "lang": lang,
    "text_vec": text_vec,
    "image_vec": image_vec,
    "doc_vec": doc_vec
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


@application.route('/')
def home():
    return render_template('application_template.html')


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
    if request.form:
        data = request.form
        text = data.get('media', None)
    else:
        data = request.get_json(force=True)
        text = data.get('text', None)

    if type(text) != str:
        ret = {'failed': 1, 'error': 'no text found'}
        return jsonify(ret)

    doc_id = data.get('doc_id', None)  # why would they give an id?
    if text is None:
        ret = {'failed': 1, 'error': 'No text field in json'}
        return jsonify(ret)

    if db_type == 'mongo':
        date = datetime.datetime.now()
    elif db_type == 'sqlite':
        date = datetime.date.today()
        doc_id = None

    textvec, lang = doc2vec(text)
    if lang == None:
        return jsonify({'failed': 1, 'error': textvec})

    if db_type == 'mongo':
        doc = default_db_doc(doc_id=doc_id, has_text=True, text=text, lang=lang)
        doc_id = doc['doc_id']
        if textvec is not None:
            doc["text_vec"] = textvec.tolist()
        docs.insert_one(doc)
    elif db_type == 'sqlite':
        with sqlDatabase(db_filename) as db:
            db.execute(
                "INSERT into documents(has_image, has_text, date_added, date_updated, textdata, lang, vec) values(?,?,?,?,?,?,?)", (0, 1, date, date, text, lang, textvec))

    # update the search index
    textsearch.update(doc_id, textvec)

    ret = {'failed': 0, 'doc_id': doc_id}
    return jsonify(ret)


@application.route('/remove_doc', methods=['POST'])
def remove_doc():
    """
    remove doc with doc_id from mongo server
    input: json with keys {'doc_id', 'pass'}
    """
    data = request.get_json(force=True)
    doc_id = data.get('doc_id', None)
    pwd = data.get('pass', None)

    if pwd == environ['DELETE_API_PASS']:
        if db_type == 'mongo':
            db.delete_one({'doc_id': doc_id})
        return True
    else:
        return False


@application.route('/find_duplicate', methods=['POST'])
def find_duplicate():
    """find duplicate match for any media and top approximate matches within threshold defined at the beginning of this file
    ? threshold as an env variable

    TODO: searches for both text and image search matches
    TODO: return multiple matches

    Returns:
        [dict] -- {'failed': 0 if failed, else 1, 'error': error string, 'doc_id': matching doc_id, 'distance': diff between embeddings, 0 if duplicate}
    """
    # force=true: ignore mimetype (media type) https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
    if request.form:
        data = request.form
        text = data.get('text', None)
        image_url = data.get('image', None)
    else:
        data = request.get_json(force=True)
        text = data.get('text', None)
        image_url = data.get('image_url', None)
    if text is None and image_url is None:
        ret = {'failed': 1, 'error': 'No text or image_url found'}

    elif image_url is not None:
        image_dict = image_from_url(image_url)
        image = image_dict['image']
        image = image.convert('RGB') #take care of png(RGBA) issue
        vec = resnet18.extract_feature(image)
        # TODO: replace with docsearch?
        doc_id, dist = imagesearch.search(vec)
        if doc_id is not None:
            ret = {'failed': 0, 'duplicate': 1,
                   'doc_id': doc_id, 'distance': dist}
        else:
            ret = {'failed': 0, 'duplicate': 0}

    elif text is not None:
        if db_type == 'mongo':
            duplicate_doc = docs.find_one({"text": text})
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

        doc_id, dist = textsearch.search(textvec.tolist())
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
    data = request.get_json()
    image_url = data.get('image_url')

    image_dict = image_from_url(image_url)
    return jsonify(detect_text(image_dict))

@application.route('/upload_image', methods=['POST'])
def upload_image():
    """
    uploads image to mongodb, sqlite
    upload image_vec and text_vec separately
    input: json with keys {'doc_id', 'image_url', 'text'}
    """
    if request.form:
        data = request.form
        image_url = data.get('media', None)
    else:
        data = request.get_json(force=True)
        image_url = data.get('image_url', None)
    doc_id = data.get('doc_id', None)

    if image_url is None:
        ret = {'failed': 1, 'error': 'No image_url found'}
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
        
        # store vecs separately, combine processing in search
        # vec = np.hstack((image_vec, text_vec)).tolist()

    if db_type == 'mongo':
        date = datetime.datetime.now()
        doc = default_db_doc(doc_id=doc_id, has_image=True,
                             image_vec=image_vec.tolist())
        docs.insert_one(doc)
        doc_id = doc['doc_id']

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
    docsearch.update(doc_id, doc_vec)
    if has_text:
        textsearch.update(doc_id, text_vec)

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
    application.run(debug=True)
    # application.run(host="0.0.0.0", port=7000)
