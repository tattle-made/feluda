import unittest
from unittest.case import skip
import core.operators.md5_hash as md5_hash

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        md5_hash.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_media_from_disk(self):
        media_file_path = r'sample_data/sample-cat-video.mp4'
        md5_hash = md5_hash.run(media_file_path)
        print(md5_hash)
        self.assertEqual(32, len(md5_hash))