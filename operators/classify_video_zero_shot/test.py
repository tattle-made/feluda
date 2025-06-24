import unittest
from unittest.case import skip

from feluda.factory import VideoFactory
from operators.classify_video_zero_shot import classify_video_zero_shot


class TestClassifyVideoZeroShot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        classify_video_zero_shot.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources
        pass

    def setUp(self):
        # Set up test video paths for reuse
        self.test_videos = {
            "cat_video_url": "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4",
            "cat_video_local": "core/operators/sample_data/sample-cat-video.mp4",
        }

    def tearDown(self):
        # Clean up any temp files created during tests
        pass

    @skip
    def test_sample_video_from_disk(self):
        video_path = VideoFactory.make_from_file_on_disk(
            self.test_videos["cat_video_local"]
        )
        labels = ["cat", "dog"]
        result = classify_video_zero_shot.run(video_path, labels)
        self.assertEqual(result.get("prediction"), "cat")

    def test_sample_video_from_url(self):
        video_path = VideoFactory.make_from_url(self.test_videos["cat_video_url"])
        labels = ["cat", "dog"]
        result = classify_video_zero_shot.run(video_path, labels)
        self.assertEqual(result.get("prediction"), "cat")

    def test_sample_video_action(self):
        video_path = VideoFactory.make_from_url(self.test_videos["cat_video_url"])
        labels = ["cat eating", "cat drinking", "cat sleeping"]
        result = classify_video_zero_shot.run(video_path, labels)
        self.assertEqual(result.get("prediction"), "cat drinking")

    def test_empty_labels_error(self):
        video_path = VideoFactory.make_from_url(self.test_videos["cat_video_url"])
        labels = []
        with self.assertRaises(ValueError):
            classify_video_zero_shot.run(video_path, labels)

    def test_invalid_file_path(self):
        invalid_video = {"path": "/path/does/not/exist.mp4"}
        labels = ["cat", "dog"]
        with self.assertRaises(FileNotFoundError):
            classify_video_zero_shot.run(invalid_video, labels)

    def test_unrelated_labels(self):
        video_path = VideoFactory.make_from_url(self.test_videos["cat_video_url"])
        labels = ["airplane", "car", "building"]  # Unrelated to video content
        result = classify_video_zero_shot.run(video_path, labels)
        # Just checking it produces a result
        self.assertIn(result.get("prediction"), labels)
