import os
import tempfile
import unittest
from unittest.case import skip

import numpy as np
from PIL import Image

from feluda.factory import AudioFactory, ImageFactory, VideoFactory


class Test(unittest.TestCase):
    # Class variables to store file paths for cleanup
    test_files = []

    @classmethod
    def setUpClass(cls):
        # Initialize list to store paths of downloaded files
        cls.test_files = []

        # Define the expected filenames based on URLs
        cls.expected_files = [
            "text-in-image-test-hindi.png",
            "cat_vid_2mb.mp4.mp4",
            "audio.wav.wav",
        ]

    @classmethod
    def tearDownClass(cls):
        temp_dir = tempfile.gettempdir()

        # Attempt to remove each downloaded file
        for filename in cls.expected_files:
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Cleaned up: {file_path}")
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")

    def setUp(self):
        # Store the file path after each download for verification
        self.temp_dir = tempfile.gettempdir()

    # @skip
    def test_image_make_from_url(self):
        image_obj = ImageFactory.make_from_url_to_path(
            "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        )
        assert image_obj["path"] is not None
        # Verify file exists
        assert os.path.exists(image_obj["path"])

    @skip
    def test_image_make_from_file_on_disk(self):
        image_path = r"core/operators/sample_data/text.png"
        image_obj = ImageFactory.make_from_file_on_disk(image_path)
        assert image_obj["image"] is not None
        assert isinstance(image_obj["image"], Image.Image)
        assert isinstance(image_obj["image_array"], np.ndarray)

    # @skip
    def test_video_make_from_url(self):
        video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        result = VideoFactory.make_from_url(video_url)
        assert result["path"] is not None
        # Verify file exists
        assert os.path.exists(result["path"])

    @skip
    def test_video_make_from_file_on_disk(self):
        video_path = r"core/operators/sample_data/sample-cat-video.mp4"
        result = VideoFactory.make_from_file_on_disk(video_path)
        assert result["path"] is not None
        assert result["path"] == video_path

    # @skip
    def test_audio_make_from_url(self):
        result = AudioFactory.make_from_url(
            "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/audio.wav"
        )
        assert result["path"] is not None
        # Verify file exists
        assert os.path.exists(result["path"])

    @skip
    def test_audio_make_from_file_on_disk(self):
        audio_path = r"core/operators/sample_data/audio.wav"
        result = AudioFactory.make_from_file_on_disk(audio_path)
        assert result["path"] is not None
        assert result["path"] == audio_path
