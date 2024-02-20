import unittest
from . import ner_extraction


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        param = {}
        ner_extraction.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_simple_text_in_hindi(self):
        text = "share plzall groupअगर किसी की दोनो किउनिया वশीवर २२थ हो या पेट में पानी২हा हो सू डाय लि सिस हो২ही हो तो उसै पूरी तरह से टीकुने की वाई वैद्य गुरसेवक सिंहহাज-থাণীदी जती हैआरा हरियाा में फ्रीफन भ० 8368489856"
        entities = ner_extraction.run(text)
        print(entities)
