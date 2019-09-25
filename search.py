import numpy as np
from tqdm import tqdm
import os
from pymongo import MongoClient
from db import mongoDB, sqlDatabase, jsonDB
import json

# TODO: pass db params as python variables or env variables?
# TODO: add mongo db url
# TODO: add json support
# ~TODO: abstract over both ImageSearch and DocSearch


class ImageSearch:
    def __init__(self, db_type, db_filename):
        self.ids = []  # id of images in vec db ~ self.vecs
        self.vecs = []  # holds all features
        self.thresh = 3  # ?
        self.db_type = db_type
        self.db_filename = db_filename
        self.build()  # builds db of features for all images in db in self.vec

    def build(self):
        """
        builds a set of image features in self.vecs
        from those stored in mongodb
        """
        if self.db_type == 'mongo':
            db = mongoDB()
            docs = db.docs

            cur = docs.find({"has_image": True})
            total_docs = cur.count()
            # TODO: mongo schema is much simpler
            # vec holds both imagevec and textvec
            for doc in tqdm(cur, total=cur.count()):
                if doc.get('image_vec') is None:
                    continue
                # print(len(doc.get('vec')))
                self.ids.append(doc.get('doc_id'))
                self.vecs.append(doc.get('image_vec'))
        elif self.db_type == 'json':
            db = json.load(self.db_filename)
            cur = db.keys()
            total_docs = len(db)
        elif self.db_type == 'sqlite':
            db = sqlDatabase(self.db_filename)
            # TODO: a nicer way to get count
            total_docs = db.query("SELECT COUNT(doc_id) from documents")[0][0]
            # TODO: adapter for sqlite to return dicts
            cur = db.query(
                "SELECT doc_id, imagevec from documents where imagevec != 'null'")
            for doc in tqdm(cur, total=total_docs):
                self.ids.append(doc[0])
                self.vecs.append(doc[1])

        self.vecs = np.array(self.vecs)

    def update(self, doc_id, vec):  # add image to vec db
        self.ids.append(doc_id)
        self.vecs = np.vstack((self.vecs, vec))

    def search(self, vec):
        """
        returns (ids, dist) of self.vecs closest to input vec
        """
        if type(vec) == list:  # why is it ever a list
            vec = np.array(vec)
        # np.broadcasting search over entire database
        dists = np.linalg.norm(self.vecs - vec, axis=1)
        idx = np.argsort(dists)
        if dists[idx[0]] < self.thresh:
            return (self.ids[idx[0]], dists[idx[0]])
        else:
            return (None, None)


class DocSearch:
    def __init__(self, db_type='mongo', db_filename=None):
        self.ids = []
        self.vecs = []
        self.thresh = 0.6
        self.db_type = db_type
        self.db_filename = db_filename
        self.build()

    def build(self):
        if self.db_type == 'mongo':
            db = mongoDB()
            docs = db.docs

            cur = docs.find({"has_text": True})
            total_docs = cur.count()
            for doc in tqdm(cur, total=total_docs):
                if doc.get('text_vec') is None:
                    continue
                self.ids.append(doc.get('doc_id'))
                self.vecs.append(doc.get('text_vec'))
            # print('len', total_docs, len(self.ids))
        elif self.db_type == 'json':
            db = json.load(self.db_filename)
            cur = db.keys()
            total_docs = len(db)
        elif self.db_type == 'sqlite':
            db = sqlDatabase(self.db_filename)
            # TODO: a nicer way to get count
            total_docs = db.query("SELECT COUNT(doc_id) from documents")[0][0]
            # TODO: adapter for sqlite to return dicts
            cur = db.query(
                "SELECT doc_id, vec from documents where vec != 'null'")
            for doc in tqdm(cur, total=total_docs):
                self.ids.append(doc[0])
                self.vecs.append(doc[1])

        self.vecs = np.array(self.vecs)

    def update(self, doc_id, vec):
        self.ids.append(doc_id)
        self.vecs = np.vstack((self.vecs, vec))

    def search(self, vec):
        if type(vec) == list:
            vec = np.array(vec)

        print('len-vecs', len(self.vecs), len(vec))
        if vec is None:
            print('vec is None')
            return (None, None)
        dists = np.linalg.norm(self.vecs - vec, axis=1)
        idx = np.argsort(dists)
        if dists[idx[0]] < self.thresh:
            return (self.ids[idx[0]], dists[idx[0]])
        else:
            return (None, None)


if __name__ == "__main__":
    search = ImageSearch()
    print(search.search(np.zeros(512).tolist()))

    search = DocSearch()
    print(search.search(np.zeros(300).tolist()))
