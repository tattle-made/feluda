import io 
from google.cloud import vision
import sys,os

GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

def detect_text(path):
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts
#    for text in texts:
#        print('\n"{}"'.format(text.description))
#
#        vertices = (['({},{})'.format(vertex.x, vertex.y)
#                    for vertex in text.bounding_poly.vertices])
#
#        print('bounds: {}'.format(','.join(vertices)))

if __name__ == "__main__":
    fname = 'data/test.jpeg'
    detect_text(fname)
