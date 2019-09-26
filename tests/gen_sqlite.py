import sqlite3
import json
import io
from tqdm import tqdm


def setup_tables(db):
    """create db for embeddings, and corresponding tables
    currently placeholders english, hindi, gujarati

    Arguments:
        db {str} -- [path/filename of db]
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # if table already exists, exit function
    # https://stackoverflow.com/questions/6190776/what-is-the-best-way-to-exit-a-function-which-has-no-return-value-in-python-be
    exist = cur.fetchone()
    if not exist:
        conn.close()
        return

    cur.execute("CREATE TABLE lang_ids (lang_id int, lang text)")
    cur.execute("insert into lang_ids values (0,'en')")
    cur.execute("insert into lang_ids values (1,'hi')")
    cur.execute("insert into lang_ids values (2,'gu')")
    cur.execute(
        "CREATE TABLE wordvecs (word text, lang_id int REFERENCES lang_ids(lang_id), vec text)")
    cur.execute("CREATE INDEX word_index ON wordvecs (word);")
    cur.execute("CREATE INDEX lang_index ON wordvecs (lang_id);")
    cur.execute("CREATE INDEX full_index ON wordvecs (word, lang_id);")
    conn.commit()
    conn.close()


def insert_words(filename, lang_id, db):
    """insert words from embeddings into db

    Arguments:
        filename {str} -- file containing embeddings
        lang_id {int} -- id for which language: {0: en, 1: hi, 2: gu}
        db {str} -- path/filename of db
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    fin = io.open(filename, 'r',
                  encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    for line in tqdm(fin, total=n):
        tokens = line.rstrip().split(' ')
        vec = json.dumps(list(map(float, tokens[1:])))
        word = tokens[0].replace("'", '"')
        try:
            cur.execute("insert into wordvecs values ('%s','%s','%s')" %
                        (word, lang_id, vec))
        except:
            print(tokens[0])
            continue
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # TODO: add eng/hi/gu files
    # ~TODO: add support for other embeddings, make it embedding agnostic
    # TODO: testing db for speed, latency
    # TODO: testing db for content

    # params
    db = 'word2vec.db'

    eng_file = 'cc.en.300.vec.gz'
    hindi_file = 'cc.hi.300.vec.gz'
    guj_file = 'cc.gu.300.vec.gz'

    # create database
    setup_tables(db)

    # insert word_vectors
    insert_words(eng_file, 0, db)
    insert_words(hindi_file, 1, db)
    insert_words(guj_file, 2, db)
