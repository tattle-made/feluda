from pymongo import MongoClient
from os.path import isfile
from os import listdir
from datetime import date
import sqlite3
import numpy as np
from io import BytesIO
# https://stackoverflow.com/questions/38076220/python-mysqldb-connection-in-a-class

# TODO: is a db agnostic wrapper worth it?


class sqlDatabase:
    """
    Database wrapper/layer to make rest of code db-agnostic

    TODO: some of the methods are quite empty, remove and use native methods
    """

    # # if table already exists, exit function
    # # https://stackoverflow.com/questions/6190776/what-is-the-best-way-to-exit-a-function-which-has-no-return-value-in-python-be
    # if not self.exists:
    #     self.__exit__()

    def setup(self):
        # https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
        def adapt_array(arr):
            """
            http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
            """
            out = BytesIO()
            np.save(out, arr)
            out.seek(0)
            return sqlite3.Binary(out.read())

        def convert_array(text):
            out = BytesIO(text)
            out.seek(0)
            return np.load(out)

        def im2bin(img):
            stream = BytesIO()
            img.save(stream, format="JPEG")
            img_bytes = stream.get_value()

        # Converts np.array to TEXT when inserting
        sqlite3.register_adapter(np.ndarray, adapt_array)

        # Converts TEXT to np.array when selecting
        sqlite3.register_converter("array", convert_array)

    def __init__(self, filename):
        self.setup()

        self.db = None
        self._conn = sqlite3.connect(
            filename, detect_types=sqlite3.PARSE_DECLTYPES)
        self._cursor = self._conn.cursor()
        self.exists = self._cursor.fetchone()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    def get_tablenames(self):
        return self.query("SELECT name FROM sqlite_master WHERE type='table'")

    def get_table_schema(self, table_name):
        return self.query(
            'SELECT sql FROM sqlite_master WHERE type="table" and name="' + table_name + '"')

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def executemany(self, sql, params=None):
        self.cursor.executemany(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def create_table(self, table_name, table_tuple):
        # table_name = lang_ids, table_tuple = (lang_id int, lang text)
        # this is a stupid method: remove
        # TODO: check if table exists
        self.cur.execute("CREATE TABLE " + table_name + " " + table_tuple)

    def insert_values(self, table_name, values):
        # this is a stupid method: remove
        query = 'insert into' + table_name + 'values' + values

    def get_db(self):
        # mongo_url = os.environ['MONGO_URL']
        # cli = MongoClient(mongo_url)
        # db = cli.documents
        return None


class mongoDB:
    def __init__(self):
        mongo_url = os.environ['MONGO_URL']
        cli = MongoClient(mongo_url)
        self.db = cli.documents


class jsonDB:
    def __init__(self, filename):
        self.filename = filename
        self.schema = {
            "doc_id": int,
            "has_image": bool,
            "has_text": bool,
            "date_added": str,
            "date_updated": str,
            "tags": list(str),
            "text": str,
            "lang": str
        }

        self.exists = isfile(self.filename)

    def build_db(folder, filetype='.txt'):
        if self.exists:
            with open(self.filename, 'w') as f:
                db = json.load(f)

        files = listdir(folder)
        files = [f for f in files if filetype in f]

        for file in files:
            with open(file, 'r') as d:
                vec = a.get_vec(f.read())
                doc_id = 10

        return


def create_mongo_db():
    client = MongoClient('localhost', 27017)
    db = client['db']

    return None


def detect_lang(text):
    import langdetect

    supported = ['en', 'hi', 'gu']
    lang = langdetect.detect(text)
    if lang not in supported:
        return None
    else:
        return lang


def create_sql_db(filename='docs_sqlite_db.db'):
    from analyzer_no_google import doc2vec
    from PIL import Image
    from analyzer_no_google import ResNet18

    db = sqlDatabase(filename)

    # https://www.tutorialspoint.com/sqlite/sqlite_data_types.htm
    insert_table_query = 'CREATE TABLE documents (doc_id integer primary key, has_image int, has_text int, date_added text, date_updated text, tags text, textdata text, lang text, vec array, imagedata blob, imagemetadata text, imagevec array)'
    db.execute(insert_table_query)

    texts_folder = listdir('tests/texts/')
    images_folder = listdir('tests/images/')

    # defaults
    has_text = 1
    has_image = 0
    date_added = date.today()
    date_updated = date.today()
    tags = None
    imagedata = None
    imagemetadata = None
    imagevec = None

    for file in texts_folder:
        with open('tests/texts/' + file, 'r') as f:
            textdata = f.read()
            if len(textdata) == 0:
                continue
            vec, lang = doc2vec(textdata, 'word2vec/word2vec.db')

            data = (has_text, has_image, date_added, date_updated,
                    tags, textdata, lang, vec, imagedata, imagemetadata, imagevec)

        db.execute('INSERT into documents(has_image, has_text, date_added, date_updated, tags, textdata, lang, vec, imagedata, imagemetadata, imagevec) values(?,?,?,?,?,?,?,?,?,?,?)', data)

    # defaults
    has_text = 0
    has_image = 1
    date_added = date.today()
    date_updated = date.today()
    tags = None
    textdata = None
    lang = None
    vec = None

    model = ResNet18()

    for file in images_folder:
        img = Image.open('tests/images/' + file)
        # assert(type(img) == Image.Image)
        imagedata = img.tobytes()
        imagemetadata = str({'mode': img.mode, 'size': img.size})
        imagevec = model.extract_feature(img)

        data = (has_text, has_image, date_added, date_updated,
                tags, textdata, lang, vec, imagedata, imagemetadata, imagevec)

        db.execute('INSERT into documents(has_image, has_text, date_added, date_updated, tags, textdata, lang, vec, imagedata, imagemetadata, imagevec) values(?,?,?,?,?,?,?,?,?,?,?)', data)

    db.commit()
    db._conn.close()
