import unittest
from . import detect_lang_of_text


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        detect_lang_of_text.initialize(param)
        pass

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_short_text(self):
        lang = detect_lang_of_text.run("")
        self.assertEqual(lang, None)

    def test_english_detection(self):
        lang = detect_lang_of_text.run("hello, how are you?")
        self.assertEqual(lang, "en")

    def test_hindi_detection(self):
        lang = detect_lang_of_text.run("नमस्ते, आप कैसे हैं?")
        self.assertEqual(lang, "hi")

    def test_gujarati_detection(self):
        lang = detect_lang_of_text.run("નમસ્તે, કેમ છો?")
        self.assertEqual(lang, "gu")

    def test_unsupported_lang_detection(self):
        lang_1 = detect_lang_of_text.run("намасте, как дела?")
        lang_2 = detect_lang_of_text.run("Ciao, come stai ?")
        lang_3 = detect_lang_of_text.run("مرحبا كيف حالك")
        self.assertEqual(lang_1, "und")
        self.assertEqual(lang_2, "und")
        self.assertEqual(lang_3, "und")
