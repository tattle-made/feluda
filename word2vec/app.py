import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os, sys, json
from pymongo import MongoClient
from textblob import TextBlob
import sqlite3

mongo_url = os.environ['MONGO_URL']
cli = MongoClient(mongo_url)
db = cli.testing

class Search:
    def __init__(self):
        self.docs = [1,2,3]
        self.vecs = []

    def search(self, text):
        v = self.doc2vec(text)
        np.argsort(np.linalg.norm(vecs - v, axis=1))

    def update(self, doc_text):
        lang = self.detect_lang(doc_text)
        vec = self.doc2vec(doc_text)
        doc = {'text' : doc_text, 'lang' : lang}
        self.docs.append(doc)
        self.vecs.append(vec)

    def doc2vec(self, text):
        """
        avg the word vectors for each word in the doc, 
        ignore the words not found in the db
        """
        conn = sqlite3.connect('aligned_vecs.db')
        cur = conn.cursor()

        # get lang_id
        lang = self.detect_lang(text)
        if lang is None:
            return None

        resp = cur.execute("select * from lang_ids where lang='"+lang+"'").fetchone()
        if resp is None:
            return None
        lang_id = resp[0]

        #query wordvecs for each word in text for that lang_id
        words = text.replace('\n',' ').replace("'","").split(' ')
        query = f"SELECT * from wordvecs where lang_id={lang_id} and word in "+\
                    '('+','.join(['\''+i+'\'' for i in words])+')'
        resp = cur.execute(query)
        if resp is None:
            return None
       
        vecs = []
        word_vecs = resp.fetchall()
        if len(word_vecs) == 0:
            return None
            #return np.zeros(300).tolist()
        else:
            for word,_,vec in word_vecs:
                vec = json.loads(vec)
                vec = np.array(vec)
                vecs.append(vec)

            mean_vec = np.mean(vecs, axis=0)
            return mean_vec.tolist()

    def detect_lang(self, text):
        if text == "" or text == " ":
            return None
        supported = ['en','hi','bn','ta']
        #lang = langdetect.detect(text)
        blob = TextBlob(text)
        lang = blob.detect_language()
        if lang not in supported:
            return None
        else:
            return lang


S = Search()
docs = []

# Sidebar
st.sidebar.markdown('Search Options')
languages = ['English', 'Hindi', 'Bangali', 'Tamil']
selected_languages = st.sidebar.multiselect('Select Languages', 
        languages, default=languages)
n_docs = st.sidebar.slider('Select Number of Documents',
                            5, 100, 10)

@st.cache
def update(text):
    docs.append(doc_text)
    S.update(doc_text)

@st.cache
def search(text):
    print(S.docs)
    print(docs)

#st.header('Add a doc')
#doc_text = st.text_input('', value='', key='add')
#if st.button('Add'):
#    update(doc_text)

st.header('Search documents')
search_text = st.text_input('', value='', key='search')
if st.button('Search'):
    search(search_text)
    pass


S.docs
S.vecs

#st.header('Reset Database')
#if st.button('RESET'):
#    pass

