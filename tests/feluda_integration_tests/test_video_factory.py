"""
Test file for the VideoFactory class, focusing on the make_from_url method
with invalid URLs
"""
import unittest
from unittest.mock import patch

from feluda.models.media_factory import VideoFactory


class TestVideoFactory(unittest.TestCase):
    """Tests for the VideoFactory class."""

    def test_invalid_video_url(self):
        """Test handling of invalid video URL."""
        invalid_url = "https://nonexistent-url/video.mp4"
        
        #simulates a download failure
        with patch("wget.download") as mock_download:
            # Configure the mock to raise an exception when called
            mock_download.side_effect = Exception("Error downloading video")
            
            # Assert that the function raises an exception
            with self.assertRaises(Exception) as context:
                VideoFactory.make_from_url(invalid_url)
            
            # Check that the exception message contains the expected text
            self.assertIn("Error Downloading Video", str(context.exception))


if __name__ == "__main__":
    unittest.main()
