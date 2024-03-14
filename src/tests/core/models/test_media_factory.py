import unittest

# from unittest.case import skip
import numpy as np
from PIL import Image
from core.models.media_factory import ImageFactory, VideoFactory, AudioFactory


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # @skip
    def test_image_make_from_url(self):
        image_obj = ImageFactory.make_from_url(
            "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        )
        self.assertIsNotNone(image_obj["image"])
        self.assertTrue(isinstance(image_obj["image"], Image.Image))
        self.assertTrue(isinstance(image_obj["image_array"], np.ndarray))

    # @skip
    def test_image_make_from_file_on_disk(self):
        image_path = r"core/operators/sample_data/text.png"
        image_obj = ImageFactory.make_from_file_on_disk(image_path)
        self.assertIsNotNone(image_obj["image"])
        self.assertTrue(isinstance(image_obj["image"], Image.Image))
        self.assertTrue(isinstance(image_obj["image_array"], np.ndarray))

    # @skip
    def test_video_make_from_url(self):
        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        result = VideoFactory.make_from_url(video_url)
        self.assertIsNotNone(result["path"])

    # @skip
    def test_video_make_from_file_on_disk(self):
        video_path = r"core/operators/sample_data/sample-cat-video.mp4"
        result = VideoFactory.make_from_file_on_disk(video_path)
        self.assertIsNotNone(result["path"])
        self.assertEqual(result["path"], video_path)

    # @skip
    def test_audio_make_from_url(self):
        result = AudioFactory.make_from_url(
            "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/audio.wav"
        )
        self.assertIsNotNone(result["path"])

    # @skip
    def test_audio_make_from_file_on_disk(self):
        audio_path = r"core/operators/sample_data/audio.wav"
        result = AudioFactory.make_from_file_on_disk(audio_path)
        self.assertIsNotNone(result["path"])
        self.assertEqual(result["path"], audio_path)
