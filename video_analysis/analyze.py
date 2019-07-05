import numpy as np
from tqdm import tqdm
import sys, os
from PIL import Image
sys.path.append('..')
from analyzer import *

model = ResNet18()

def img2vec(fname):
    img = Image.open(fname)
    vec = model.extract_feature(img)
    return vec

vecs = []
for fname in tqdm(os.listdir('samples')):
    v = img2vec('samples/'+fname)
    vecs.append(v)

X = np.array(vecs)
print(X.shape)
