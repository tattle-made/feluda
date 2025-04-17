import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import yaml

from feluda import Feluda
from feluda.models.media_factory import VideoFactory



class TestFeludaVideoVectorIntegration(unittest.TestCase):
    """Integration tests for Feluda's video vector representation using CLIP."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        # Configuration for feluda with the video vector operator
        cls.config = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "video vectors",
                        "type": "vid_vec_rep_clip",
                        "parameters": {"index_name": "video"},
                    }
                ],
            }
        }

        # Create temporary config file
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        # Initialize Feluda
        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()

        # Test constants
        cls.test_video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"

    def setUp(self):
        """Set up test-specific resources."""
        # Get operator reference in each test to ensure isolation
        self.operator = self.feluda.operators.get()["vid_vec_rep_clip"]

    def test_invalid_video_url(self):
        """Test handling of invalid video URL.
        
        This test verifies that when an invalid video URL is provided,
        the VideoFactory.make_from_url method raises an exception with
        the correct error message.
        
        This is the core issue that was fixed in PR #569.
        """
        invalid_url = "https://nonexistent-url/video.mp4"

        # Use patch to mock the wget.download function to simulate a download failure
        with patch("wget.download") as mock_download:
            # Configure the mock to raise an exception when called
            mock_download.side_effect = Exception("Error downloading video")
            
            # Assert that the function raises an exception
            with self.assertRaises(Exception) as context:
                VideoFactory.make_from_url(invalid_url)
            
            # Check that the exception message contains the expected text
            # This is the key fix from PR #569
            self.assertIn("Error Downloading Video", str(context.exception))

    def test_operator_configuration(self):
        """Test that operator is properly configured."""
        self.assertIsNotNone(self.operator, "Operator should be properly initialized")
        self.assertTrue(
            hasattr(self.operator, "run"), "Operator should have 'run' method"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests are complete."""
        try:
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
