import unittest
from unittest.case import skip
from core.models.media_factory import AudioFactory
from core.operators import audio_vec_embedding


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        audio_vec_embedding.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    @skip
    def test_sample_audio_from_disk(self):
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/audio.wav"
        )
        audio_emb = audio_vec_embedding.run(audio_file_path)
        self.assertEqual(2048, len(audio_emb))

    # @skip
    def test_sample_audio_from_url(self):
        audio_path = AudioFactory.make_from_url(
            "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/audio.wav"
        )
        audio_emb = audio_vec_embedding.run(audio_path)
        self.assertEqual(2048, len(audio_emb))
