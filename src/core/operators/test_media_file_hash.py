import unittest
from unittest.case import skip
from core.operators import media_file_hash
from core.models.media_factory import VideoFactory


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        media_file_hash.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    @skip
    def test_sample_media_from_disk(self):
        media_file_path = VideoFactory.make_from_file_on_disk("core/operators/sample_data/sample-cat-video.mp4")
        hash = media_file_hash.run(media_file_path)
        self.assertEqual(128, len(hash))

    # @skip
    def test_sample_media_from_url(self):
        media_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        media_path = VideoFactory.make_from_url(media_url)
        hash = media_file_hash.run(media_path)
        self.assertEqual(128, len(hash))
