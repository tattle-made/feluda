import sqlite3, json, io
from tqdm import tqdm


def setup_tables():
    conn = sqlite3.connect('word2vec.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE lang_ids (lang_id int, lang text)")
    cur.execute("insert into lang_ids values (0,'en')")
    cur.execute("insert into lang_ids values (1,'hi')")
    cur.execute("insert into lang_ids values (2,'gu')")
    cur.execute("CREATE TABLE wordvecs (word text, lang_id int REFERENCES lang_ids(lang_id), vec text)")
    cur.execute("CREATE INDEX word_index ON wordvecs (word);")
    cur.execute("CREATE INDEX lang_index ON wordvecs (lang_id);")
    cur.execute("CREATE INDEX full_index ON wordvecs (word, lang_id);")
    conn.commit()
    conn.close()


def insert_words():
    conn = sqlite3.connect('word2vec.db')
    cur = conn.cursor()
    fin = io.open('/data/word2vec/cc.en.300.vec', 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    for line in tqdm(fin,total=n):
        tokens = line.rstrip().split(' ')
        vec = json.dumps(list(map(float, tokens[1:])))
        word = tokens[0].replace("'",'"')
        try:
            cur.execute("insert into wordvecs values ('%s',0,'%s')" % (word, vec))
        except:
            print(tokens[0])
            continue
            import ipdb; ipdb.set_trace()
    conn.commit()
    conn.close()

insert_words()
