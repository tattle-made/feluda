import io 
from io import BytesIO
import sys,os,json
from google.cloud import vision
from google.protobuf.json_format import MessageToJson
import torchvision.models as models
import torch 
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
import numpy as np
from textblob import TextBlob
import requests
import skimage, PIL
import sqlite3
from monitor import timeit
import boto3

def get_credentials():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY_ID")
    bucket = os.environ.get("AWS_BUCKET")
    obj = os.environ.get("S3_CREDENTIALS_PATH")
    s3 = boto3.client("s3", aws_access_key_id = aws_access_key_id,
                          aws_secret_access_key= aws_secret_access_key) 
    s3.download_file(bucket, obj, "credentials.json")

GOOGLE_API_KEY=get_credentials()

#imagenet normalize
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
scaler = transforms.Resize((224, 224))
to_tensor = transforms.ToTensor()

@timeit
def image_from_url(image_url):
    resp = requests.get(image_url)
    image_bytes = resp.content
    image = PIL.Image.open(BytesIO(image_bytes))
    image_array = np.array(image)
    return {'image' : image, 'image_array' : image_array, 'image_bytes' : image_bytes}

class ResNet18():
    def __init__(self):
        self.model = models.resnet18(pretrained=True)
        self.feature_layer = self.model._modules.get('avgpool')
        self.model.eval()

    def extract_feature(self, img):
        img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
        embedding = torch.zeros(512)
        def hook(m, i, o):
            feature_data = o.data.reshape((512))
            embedding.copy_(feature_data)
        h = self.feature_layer.register_forward_hook(hook)
        self.model(img)
        h.remove()
        embedding_fp16 = np.array(embedding.numpy(), dtype=np.float16)
        return embedding_fp16

def detect_text(img_bytes):
    client = vision.ImageAnnotatorClient()
    image_data = vision.types.Image(content=img_bytes)
    resp = client.text_detection(image=image_data)
    resp = json.loads(MessageToJson(resp))
    text = resp.get('fullTextAnnotation',{}).get('text','')
    return {'text' : text, 'full' : resp}
#    for text in texts:
#        print('\n"{}"'.format(text.description))
#
#        vertices = (['({},{})'.format(vertex.x, vertex.y)
#                    for vertex in text.bounding_poly.vertices])
#
#        print('bounds: {}'.format(','.join(vertices)))

def transform_text(text, sent_model):
    """
    New method for generating text document vectors.
    """
    vec = sent_model.encode(text)
    return vec

def doc2vec(text):
    """
    Old method for generating text document vectors.
    avg the word vectors for each word in the doc, 
    ignore the words not found in the db
    """
    conn = sqlite3.connect('data/word2vec/word2vec.db')
    print(conn)
    cur = conn.cursor()
    print(cur)

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
    # get lang_id
    lang = detect_lang(text)
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

def detect_lang(text):
    if text == "" or text == " " or len(text) < 3:
        return None
    supported = ['en','hi','gu']
    #lang = langdetect.detect(text)
    blob = TextBlob(text)
    lang = blob.detect_language()
    if lang not in supported:
        return None
    else:
        return lang

if __name__ == "__main__":
    text = "what is this"
    vec = doc2vec(text)
    print(vec)

    text="बिल्कुल सोच समझ कर "
    vec = doc2vec(text)
    print(vec)

 
    from PIL import Image
    import skimage.io

    model = ResNet18()
    url = "https://firebasestorage.googleapis.com/v0/b/crowdsourcesocialposts.appspot.com/o/image-posts%2F06c1eaa0-feea-42e5-8eee-b3ab3b099831?alt=media&token=cf1b9b4f-fa1f-48e4-8d64-82476cfeec1a"
    img = Image.fromarray(skimage.io.imread(url))
    fnames = ['01545ee202e12f8435d4a0997f4072c370de0897.jpg',
              '01545ee202e12f8435d4a0997f4072c370de0897_1.jpg',
              '01545ee202e12f8435d4a0997f4072c370de0897_2.jpg',
              '01545ee202e12f8435d4a0997f4072c370de0897_3.jpg',
              'efe1cf7044079d2dac7f8f1294f71f9244d42f80.jpg']

    imgs = [Image.open('tests/images/'+i) for i in fnames]
    features = [model.extract_feature(img) for img in imgs]

    for f in features[1:]:
        print(np.linalg.norm(f - features[0]))

    #resp = detect_text('tests/images/6f6de48ffce515c6dd75d162634b9177d693c8ef.jpg')
    import IPython

    img_dict = image_from_url(url)
    resp = detect_text(img_dict['image_bytes'])
    print(resp)

    IPython.embed()
    sys.exit()
    #fname = 'data/test.jpeg'
