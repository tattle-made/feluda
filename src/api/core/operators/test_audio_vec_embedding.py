import unittest
from unittest.case import skip
import audio_vec_embedding

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        audio_vec_embedding.initialize(param={})
    
    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_audio_from_disk(self):
        audio_file_path = r'sample_data/audio.wav'
        audio_emb = audio_vec_embedding.run(audio_file_path)
        self.assertEqual(2048, len(audio_emb))