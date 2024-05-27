import unittest
from core.models.media_factory import AudioFactory
from core.operators import detect_lang_of_audio

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        detect_lang_of_audio.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_english_detection(self):
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/en_speech.wav"
        )
        lang = detect_lang_of_audio.run(audio_file_path)
        self.assertEqual(lang["id"], "en")
        self.assertEqual(lang["language"], "english")

    def test_hindi_detection(self):
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/hi_speech.wav"
        )
        lang = detect_lang_of_audio.run(audio_file_path)
        self.assertEqual(lang["id"], "hi")
        self.assertEqual(lang["language"], "hindi")

    def test_tamil_detection(self):
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/ta_speech.wav"
        )
        lang = detect_lang_of_audio.run(audio_file_path)
        self.assertEqual(lang["id"], "ta")
        self.assertEqual(lang["language"], "tamil")

    def test_telugu_detection(self):
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/te_speech.wav"
        )
        lang = detect_lang_of_audio.run(audio_file_path)
        self.assertEqual(lang["id"], "te")
        self.assertEqual(lang["language"], "telugu")

    def test_speech_extraction_in_heterogeneous_audio(self):
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/hi_speech_after_30s_music.wav"
        )
        lang = detect_lang_of_audio.run(audio_file_path)
        self.assertEqual(lang["id"], "hi")
        self.assertEqual(lang["language"], "hindi")