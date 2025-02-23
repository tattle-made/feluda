import unittest
from detect_audio_fingerprint import convert, spectrogram, fingerprint

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        pass

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_audio_from_disk(self):
        convert(r'sample_data/audio.mp3')
        audio_file = r'sample_data/audio.wav'
        _, f_v, _, spect_v = spectrogram(audio_file)
        fingerprint_v = fingerprint(f_v, spect_v)
        self.assertEqual(len(fingerprint_v), 2)

