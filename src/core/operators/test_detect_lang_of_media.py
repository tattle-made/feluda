import unittest
from core.models.media_factory import AudioFactory,VideoFactory
from core.operators import detect_lang_of_media

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        detect_lang_of_media.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_english_detection_audio(self):
        audio_file_path = AudioFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/en_speech.wav"
            
        )
        lang = detect_lang_of_media.run(audio_file_path,'audio')
        self.assertEqual(lang["id"], "en")
        self.assertEqual(lang["language"], "english")

    def test_english_detection_video(self):
        audio_file_path = VideoFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/en-speech.mp4"
        )
        lang = detect_lang_of_media.run(audio_file_path,'video')
        self.assertEqual(lang["id"], "en")
        self.assertEqual(lang["language"], "english")


    def test_hindi_detection_video(self):
        audio_file_path = VideoFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/hi-speech.mp4"
            
        )
        lang = detect_lang_of_media.run(audio_file_path,'video')
        self.assertEqual(lang["id"], "hi")
        self.assertEqual(lang["language"], "hindi")

    def test_hindi_detection_audio(self):
        audio_file_path = AudioFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/hi_speech.wav"
        )
        lang = detect_lang_of_media.run(audio_file_path,'audio')
        self.assertEqual(lang["id"], "hi")
        self.assertEqual(lang["language"], "hindi")


    def test_tamil_detection_audio(self):
        audio_file_path = AudioFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/ta_speech.wav"
        )
        lang = detect_lang_of_media.run(audio_file_path,'audio')
        self.assertEqual(lang["id"], "ta")
        self.assertEqual(lang["language"], "tamil")

    def test_tamil_detection_video(self):
        audio_file_path = VideoFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/ta_speech.mp4"
        )
        lang = detect_lang_of_media.run(audio_file_path,'video')
        self.assertEqual(lang["id"], "ta")
        self.assertEqual(lang["language"], "tamil")

    def test_telugu_detection_audio(self):
        audio_file_path = AudioFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/te_speech.wav"
        )
        lang = detect_lang_of_media.run(audio_file_path,'audio')
        self.assertEqual(lang["id"], "te")
        self.assertEqual(lang["language"], "telugu")

    def test_telugu_detection_video(self):
        audio_file_path = VideoFactory.make_from_file_on_disk(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/te_speech.mp4"
        )
        lang = detect_lang_of_media.run(audio_file_path,'video')
        self.assertEqual(lang["id"], "te")
        self.assertEqual(lang["language"], "telugu")

    def test_speech_extraction_in_heterogeneous_audio(self):
        audio_file_path = AudioFactory.make_from_url(
            r"https://github.com/aatmanvaidya/audio-files/raw/main/feluda-media/hi_speech_after_30s_music.wav"
        )
        lang = detect_lang_of_media.run(audio_file_path,'audio')
        self.assertEqual(lang["id"], "hi")
        self.assertEqual(lang["language"], "hindi")