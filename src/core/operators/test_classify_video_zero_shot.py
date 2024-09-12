import unittest
from unittest.case import skip
from src.core.operators import classify_video_zero_shot
from core.models.media_factory import VideoFactory


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        classify_video_zero_shot.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    @skip
    def test_sample_video_from_disk(self):
        video_path = VideoFactory.make_from_file_on_disk(
            r"core/operators/sample_data/sample-cat-video.mp4"
        )
        labels = [ "cat", "dog" ]
        result = classify_video_zero_shot.run(video_path, labels)
        self.assertEqual(result.get("prediction"), "cat")

    # @skip
    def test_sample_video_from_url(self):
        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        video_path = VideoFactory.make_from_url(video_url)
        labels = [ "cat", "dog" ]
        result = classify_video_zero_shot.run(video_path, labels)
        self.assertEqual(result.get("prediction"), "cat")
