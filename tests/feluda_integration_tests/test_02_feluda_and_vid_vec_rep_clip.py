import contextlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import yaml
from requests.exceptions import ConnectTimeout

from feluda import Feluda
from feluda.models.media_factory import VideoFactory


class TestFeludaVideoVectorIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""
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

        # Create temporary config file using with statement to ensure proper resource cleanup
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        # Initialize Feluda
        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()

        cls.test_video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        cls.expected_vector_dim = 512

    def setUp(self):
        """Set up test-specific feluda resources."""
        # Get operator reference in each test to ensure isolation
        self.operator = self.feluda.operators.get()["vid_vec_rep_clip"]

    def test_video_vector_generation(self):
        """Test that video vector generation works end-to-end."""
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video_obj, "Video object should be successfully created")

        # Get the first vector from the generator
        video_vec = next(self.operator.run(video_obj))

        self.assertTrue(
            "vid_vec" in video_vec,
            "Result should contain 'vid_vec' key",
        )
        self.assertTrue(
            "is_avg" in video_vec,
            "Result should contain 'is_avg' key",
        )
        
        vid_vec = video_vec["vid_vec"]
        self.assertTrue(
            isinstance(vid_vec, list),
            "Vector should be a list",
        )
        self.assertTrue(len(vid_vec) > 0, "Vector should not be empty")
        self.assertEqual(
            len(vid_vec),
            self.expected_vector_dim,
            f"Vector should have dimension {self.expected_vector_dim}",
        )

    def test_invalid_video_url(self):
        """Test handling of invalid video URL."""
        invalid_url = "https://nonexistent-url/video.mp4"
        
        with patch("wget.download") as mock_download:
            mock_download.side_effect = Exception("Error downloading video")
            with self.assertRaises(Exception) as context:
                VideoFactory.make_from_url(invalid_url)
            self.assertIn("Error Downloading Video", str(context.exception))

    def test_operator_configuration(self):
        """Test that operator is properly configured."""
        self.assertIsNotNone(self.operator, "Operator should be properly initialized")
        self.assertTrue(
            hasattr(self.operator, "run"), "Operator should have 'run' method"
        )

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        """Context manager to verify no exception is raised."""
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Exception was raised'}: {e}")

    def test_video_vector_consistency(self):
        """Test that generating vectors twice from the same video gives consistent results."""
        video_obj = VideoFactory.make_from_url(self.test_video_url)

        with self.assertNoException(
            "First vector generation should not raise exceptions"
        ):
            # Convert generator to list to get all vectors
            vec1 = list(self.operator.run(video_obj))
            # Get the average vector (first one, is_avg=True)
            avg_vec1 = vec1[0]["vid_vec"]

        # Need to get a fresh video object since the previous one was consumed
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        
        with self.assertNoException(
            "Second vector generation should not raise exceptions"
        ):
            # Convert generator to list to get all vectors
            vec2 = list(self.operator.run(video_obj))
            # Get the average vector (first one, is_avg=True)
            avg_vec2 = vec2[0]["vid_vec"]

        # Compare the average vectors
        self.assertEqual(len(avg_vec1), len(avg_vec2), "Vector dimensions should match")
        np.testing.assert_allclose(
            avg_vec1, avg_vec2, rtol=1e-5, 
            err_msg="Vectors should be very similar for the same video"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests are done."""
        try:
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
