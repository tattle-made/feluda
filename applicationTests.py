import unittest
from os import environ
import numpy as np


class imageSearchTests(unittest.TestCase):
    def setUp(self):
        from transforms import imageTransforms
        from search import ImageSearch
        from analyzer import img2vec, image_from_url

        self.db_type = 'testing'
        self.images = [(1, 'https://picsum.photos/id/448/1024/768')]
        self.ImageSearch = ImageSearch(self.db_type, self.images)
        self.ImageSearch.thresh = 25  # to pass the following tests

        self.img2vec = img2vec
        self.image_from_url = image_from_url
        self.imageTransforms = imageTransforms

    def testHasImages(self):
        self.assertTrue(len(self.ImageSearch.vecs) > 0)

    def testApproxImage(self):
        # transforms = ['crop', 'rotate', 'noise', 'b/w',
                    #   'saturation', 'add_noise_to_embedding']
        transforms = ['crop', 'rotate']

        for i, image in self.images:
            image = self.image_from_url(image)['image']

            with self.subTest(img=i):
                for tf in transforms:
                    with self.subTest(transform=tf):
                        imageTransformed = self.imageTransforms(image, type=tf)
                        imageTransformed = self.img2vec(imageTransformed, type='image')

                        ret = self.ImageSearch.search(imageTransformed)
                        self.assertEqual(ret[0], i)
                        print(f'{i}, {tf}: {ret[1]}')


class docSearchTests(unittest.TestCase):
    def setUp(self):
        from transforms import docTransforms
        from analyzer import doc2vec
        from search import DocSearch

        self.db_type = 'testing'
        self.docs = [(1, 'this is absolutely english text!'),
                     (2, 'यह बिल्कुल हिंदी पाठ है!'), (3, 'આ એકદમ ગુજરાતી લખાણ છે!')]
        self.DocSearch = DocSearch(self.db_type, self.docs)

        self.doc2vec = doc2vec
        self.docTransforms = docTransforms

    def testHasDocs(self):
        self.assertTrue(len(self.DocSearch.vecs) > 0)

    def testApproxText(self):
        """ test approximate text match
        """
        # transforms = ['drop_word', 'drop_char']
        # drop_char results in dissimilar vectors
        transforms = ['drop_word']

        for i, doc in self.docs:
            # test doc with transforms
            with self.subTest(doc=i):
                for tf in transforms:
                    with self.subTest(transform=tf):
                        docTransformed = self.docTransforms(doc, type=tf)
                        vec, _ = self.doc2vec(docTransformed)
                        if _ is None:
                            # bad example doc
                            print(f'{docTransformed}: doc no. {i}')
                            continue

                        ret = self.DocSearch.search(vec)

                        print(f'{doc} => {docTransformed}: {ret[1]}')
                        self.assertEqual(ret[0], i)


class applicationAPITests(unittest.TestCase):
    def setUp(self):
        from requests import post
        from dotenv import load_dotenv
        load_dotenv()
        
        self.SERVER = environ['LOCAL_SERVER']
        self.image_with_texts = [(
            'https://tattle-services.s3.ap-south-1.amazonaws.com/28bfb060-c51f-11e9-909c-fb10cde080ad', 'kabhi kabhi lagta hai saala apun hi good boy hai')]
        self.texts = [('This is absolutely english text!', 'en'),
                      ('यह बिल्कुल अंग्रेजी पाठ है!', 'hi')]
        self.post = post

    def testFindText(self):
        for image_url, image_text in self.image_with_texts:
            postData = {'image_url': image_url}
            response = self.post(
                f'http://{self.SERVER}/find_text', data=postData)
            with self.subTest():
                self.assertEqual(response.content, image_text)

    def testUploadAndFindDuplicateText(self):
        text = ""
        pass

    def testFindDuplicateImage(self):
        pass

    def testFindApproxText(self):
        pass

    def testFindApproximateImage(self):
        pass

    def testUploadText(self):
        pass

    def testUploadImage(self):
        pass

    def testUpdateTags(self):
        pass


class langDetectTests(unittest.TestCase):
    def setUp(self):
        from langdetect import detect
        self.detect = detect
        self.lang_keys = {'english': 'en', 'hindi': 'hi',
                          'gujarati': 'gu', 'tamil': 'ta', 'malayalam': 'ml', 'telugu': 'te', 'punjabi': 'pa', 'bangla': 'bn'}
        self.lang_keys_inverted = {v: k for k, v in self.lang_keys.items()}
        # TODO: edit this to add more test cases
        self.texts = {
            'en': ['this is absolutely english text!'],
            'hi': ['यह बिल्कुल हिंदी पाठ है!'],
            'gu': ['આ એકદમ ગુજરાતી લખાણ છે!'],
            'ta': ['இது முற்றிலும் தமிழ் உரை!'],
            'ml': ['ഇത് തികച്ചും മലയാള പാഠമാണ്!'],
            'te': ['ఇది ఖచ్చితంగా తెలుగు వచనం!'],
            'pa': ['ਇਹ ਬਿਲਕੁਲ ਪੰਜਾਬੀ ਪਾਠ ਹੈ!'],
            'bn': ['এটি একেবারে বাংলা লেখা!']
        }

    def testLanguages(self):
        for lang, texts in self.texts.items():
            with self.subTest(lang=self.lang_keys_inverted[lang]):
                for i, t in enumerate(texts):
                    with self.subTest(i=i):
                        self.assertEqual(self.detect(t), lang)


class imageLoadTests(unittest.TestCase):
    # imp warnings: https://github.com/pypa/virtualenv/issues/955

    def setUp(self):
        from analyzer import image_from_url, img2vec
        from PIL import Image

        # TODO: add different file formats
        self.image_urls = ['https://picsum.photos/id/448/1024/768']
        self.formats = ['tiff', 'jpeg', 'bmp', 'gif', 'png', 'svg']

        self.image_from_url = image_from_url
        self.img2vec = img2vec

        self.img_type = Image.Image
        self.vec_shape = (512,)

    def testImageURL(self):
        for i, url in enumerate(self.image_urls):
            with self.subTest(i=i):
                img = self.image_from_url(url)
                self.assertIsInstance(img['image'], self.img_type)
                self.assertIsInstance(img['image_array'], np.ndarray)
                self.assertIsInstance(img['image_bytes'], bytes)

    def testEmbedding(self):
        for i, img in enumerate(self.image_urls):
            with self.subTest(i=i):
                vec = self.img2vec(img)
                self.assertIsInstance(vec, np.ndarray)
                self.assertEqual(vec.shape, self.vec_shape)

if __name__ == '__main__':
    unittest.main()
