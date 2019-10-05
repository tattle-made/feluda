import json, io
from tqdm import tqdm
sample = 500
fin = io.open('cc.hi.300.vec', 'r', encoding='utf-8', newline='\n', errors='ignore')
n, d = map(int, fin.readline().split())

data = {}

count = 0
for line in tqdm(fin, total=sample):
    if count > sample:
        break
    count+=1
    tokens = line.rstrip().split(' ')
    vec = list(map(float, tokens[1:]))
    word = tokens[0]
    data[word] = vec

with open('sample.json','w') as f:
    f.write(json.dumps(data))
