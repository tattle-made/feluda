import os
import urllib.request
import hashlib

image_urls = [i.strip() for i in open('image_urls.txt').readlines()]
text_urls = [i.strip() for i in open('text_urls.txt').readlines()]

def url_to_fname(url):
    return hashlib.sha1(bytes(url, 'utf-8')).hexdigest()

for url in image_urls:
    fname = url_to_fname(url)+'.jpg'
    if not os.path.exists(os.path.join('images',fname)):
        urllib.request.urlretrieve(url, os.path.join('images',fname))

for url in text_urls:
    fname = url_to_fname(url)+'.txt'
    if not os.path.exists(os.path.join('texts',fname)):
        data = urllib.request.urlopen(url).read().decode('utf-8')
        with open(os.path.join('texts',fname),'w') as f:
            f.write(data)
