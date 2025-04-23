import os
import unittest

from feluda.models.media_factory import VideoFactory
from operators.video_hashing import video_hashing


class TestVideoHashing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        video_hashing.initialise(param=None)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_video_hashing_from_url(self):
        video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        video_obj = VideoFactory.make_from_url(video_url)
        video_path = video_obj["path"]

        # Ensure the video file exists
        self.assertTrue(os.path.exists(video_path))

        # Generate the hash
        video_hash = video_hashing.run(video_path)
        print(f"VIDEO HASSHHHHHH {len(video_hash)}")
        self.assertIsNotNone(video_hash)
        self.assertTrue(isinstance(video_hash, str))

        self.assertTrue(
            all(
                c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
                for c in video_hash
            )
        )
