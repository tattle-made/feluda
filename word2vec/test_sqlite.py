import sqlite3, json, io
from tqdm import tqdm

conn = sqlite3.connect('hindi.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE word2vec (word text, vec text)''')

fin = io.open('/data/word2vec/cc.hi.300.vec', 'r', encoding='utf-8', newline='\n', errors='ignore')
n, d = map(int, fin.readline().split())
for line in tqdm(fin,total=n):
    tokens = line.rstrip().split(' ')
    vec = json.dumps(list(map(float, tokens[1:])))
    word = json.dumps(tokens[0])
    try:
        cur.execute("insert into word2vec values ('%s','%s')" % (word, vec))
    except:
        continue

#data = json.loads(open('sample.json').read())
#for word,vec in data.items():
#    #print(word)
#    print("insert into word2vec values (%s,'%s')" % (word, vec))
#    try:
#        cur.execute("insert into word2vec values ('%s','%s')" % (word, vec))
#    except:
#        continue
conn.commit()
conn.close()
