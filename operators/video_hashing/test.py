import os
import tempfile
import unittest

from feluda.models.media_factory import VideoFactory
from operators.video_hashing.video_hashing import hash_video


class TestVideoHashing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Temporary directory for downloaded files
        cls.temp_dir = tempfile.gettempdir()

    @classmethod
    def tearDownClass(cls):
        # Clean up any leftover files in the temp directory
        for file in os.listdir(cls.temp_dir):
            if file.endswith(".mp4"):
                try:
                    os.remove(os.path.join(cls.temp_dir, file))
                except Exception as e:
                    print(f"Error cleaning up file {file}: {e}")

    def test_video_hashing_from_url(self):
        # Hosted video link
        video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"

        # Download the video using VideoFactory
        video_obj = VideoFactory.make_from_url(video_url)
        video_path = video_obj["path"]

        # Ensure the video file exists
        self.assertTrue(os.path.exists(video_path))

        # Generate the hash
        video_hash = hash_video(video_path)
        self.assertIsNotNone(video_hash)
        self.assertTrue(isinstance(video_hash, str))

        # Ensure the hash is Base64-encoded
        self.assertTrue(all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in video_hash))

        # Delete the video file after processing
        if os.path.exists(video_path):
            os.remove(video_path)

        # Ensure the file is deleted
        self.assertFalse(os.path.exists(video_path))


if __name__ == "__main__":
    unittest.main()
