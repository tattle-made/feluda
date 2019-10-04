import numpy as np
from tqdm import tqdm
import os
from pymongo import MongoClient

class ImageSearch:
    def __init__(self):
        self.ids = []
        self.vecs = []
        self.thresh = 3
        self.build()

    def build(self):
        mongo_url = os.environ['MONGO_URL']
        cli = MongoClient(mongo_url)
        db = cli.documents
        cur = db.docs.find({"has_image" : True})
        for doc in tqdm(cur, total=cur.count()):
            if doc.get('vec') is None:
                continue
            #print(len(doc.get('vec')))
            self.ids.append(doc.get('doc_id'))
            self.vecs.append(doc.get('image_vec'))

        self.vecs = np.array(self.vecs)
        
    def update(self, doc_id, vec):
        self.ids.append(doc_id)
        if len(self.vecs) == 0:
            self.vecs = np.array([vec])
        else:
            self.vecs = np.vstack((self.vecs,vec))

    def search(self, vec):
        if type(vec) == list:
            vec = np.array(vec)
        dists = np.linalg.norm(self.vecs - vec, axis=1)
        idx = np.argsort(dists)
        if dists[idx[0]] < self.thresh:
            return (self.ids[idx[0]], dists[idx[0]])
        else:
            return (None, None)

class TextSearch:
    def __init__(self):
        self.ids = []
        self.vecs = []
        self.thresh = 0.6
        self.build()

    def build(self):
        mongo_url = os.environ['MONGO_URL']
        cli = MongoClient(mongo_url)
        db = cli.documents
        cur = db.docs.find({"has_text" : True})
        for doc in tqdm(cur, total=cur.count()):
            if doc.get('vec') is None:
                continue
            self.ids.append(doc.get('doc_id'))
            self.vecs.append(doc.get('text_vec'))

        self.vecs = np.array(self.vecs)
        
    def update(self, doc_id, vec):
        self.ids.append(doc_id)
        if len(self.vecs) == 0:
            self.vecs = np.array([vec])
        else:
            self.vecs = np.vstack((self.vecs,vec))

    def search(self, vec):
        if type(vec) == list:
            vec = np.array(vec)

        if vec is None:
            print('vec is None')
            return (None, None)
        dists = np.linalg.norm(self.vecs - vec, axis=1)
        idx = np.argsort(dists)
        if dists[idx[0]] < self.thresh:
            return (self.ids[idx[0]], dists[idx[0]])
        else:
            return (None, None)

class DocSearch:
    def __init__(self):
        self.ids = []
        self.vecs = []
        self.thresh = 0.6
        self.build()

    def build(self):
        mongo_url = os.environ['MONGO_URL']
        cli = MongoClient(mongo_url)
        db = cli.documents
        cur = db.docs.find({"has_text" : True, "has_image" : True})
        for doc in tqdm(cur, total=cur.count()):
            if doc.get('vec') is None:
                continue
            self.ids.append(doc.get('doc_id'))
            self.vecs.append(doc.get('vec'))

        self.vecs = np.array(self.vecs)
        
    def update(self, doc_id, vec):
        self.ids.append(doc_id)
        if len(self.vecs) == 0:
            self.vecs = np.array([vec])
        else:
            self.vecs = np.vstack((self.vecs,vec))

    def search(self, vec):
        if type(vec) == list:
            vec = np.array(vec)

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
    print(search.search(np.zeros(812).tolist()))

    search = TextSearch()
    print(search.search(np.zeros(300).tolist()))
