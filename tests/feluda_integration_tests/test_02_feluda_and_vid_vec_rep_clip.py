# Standard library imports
import contextlib  # For creating context managers
import tempfile  # For creating temporary files
import unittest  # For creating test cases
from pathlib import Path  # For file path operations

import numpy as np  # For numerical operations and array comparisons
import yaml  # For YAML file operations

from feluda import Feluda
from feluda.models.media_factory import (
    VideoFactory,  # Factory for creating video objects
)


class TestFeludaVideoVectorIntegration(unittest.TestCase):
    """Integration tests for Feluda's video vector representation using CLIP.

    This test suite verifies that the vid_vec_rep_clip operator correctly generates
    vector representations of videos, handles errors appropriately, and produces
    consistent results across multiple runs."""
    @classmethod
    def setUpClass(cls):
        """Creates a temporary test configuration file that will be used for all tests.

        This method is called once before any tests in the class are run.
        It sets up a Feluda instance with the vid_vec_rep_clip operator.

        The setup process includes:
        1. Creating a configuration dictionary with the vid_vec_rep_clip operator
        2. Writing this configuration to a temporary YAML file
        3. Setting up test constants like the test video URL and expected vector dimension
        """
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

        # Create temporary config file using with statement to ensure proper resource cleanup
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)  # writes the configuration to the temporary file

        # Initialize Feluda
        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()

        # Test constants
        cls.test_video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"  # URL to the test video
        cls.expected_vector_dim = 512  # Expected dimension of the CLIP video vectors

    def setUp(self):
        """Set up test-specific feluda resources.

        This method is called before each test method is executed.
        It initializes the operator reference for each test.
        """
        # Get operator reference in each test to ensure isolation
        self.operator = self.feluda.operators.get()["vid_vec_rep_clip"]

    def test_video_vector_generation(self):
        """Test that video vector generation works end-to-end.

        This test verifies the complete pipeline of:
        1. Creating a video object from a URL
        2. Generating vector representations using the vid_vec_rep_clip operator
        3. Validating the properties of the generated vectors

        The test checks:
        - That a video object can be created from the URL
        - That at least one vector is generated (the average vector)
        - That the vectors have the correct format and dimensions
        - That the first vector is marked as the average vector
        - That all vectors have the expected dimension
        """
        # Create a video object from the test URL
        video = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video, "Video object should be successfully created")

        # Generate vectors using the operator
        vectors = list(self.operator.run(video))

        # Basic validation
        self.assertGreater(len(vectors), 0, "No vectors were generated")

        # Check the first vector (should be the average vector)
        first_vector = vectors[0]
        self.assertTrue(first_vector["is_avg"], "First vector should be marked as average")
        self.assertEqual(
            len(first_vector["vid_vec"]),
            self.expected_vector_dim,
            "Average vector has incorrect dimension",
        )

        # Check all other vectors
        for vector in vectors[1:]:
            self.assertFalse(vector["is_avg"], "Non-first vector marked as average")
            self.assertEqual(
                len(vector["vid_vec"]),
                self.expected_vector_dim,
                "Frame vector has incorrect dimension",
            )

    def test_invalid_video_url(self):
        """Test handling of invalid video URL."""
        invalid_url = "https://nonexistent-url/video.mp4"

        # Direct test with invalid URL
        result = VideoFactory.make_from_url(invalid_url)
        self.assertIsNone(result, "Invalid URL should return None")

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
        # Create a video object for testing
        video = VideoFactory.make_from_url(self.test_video_url)

        # First generation
        with self.assertNoException("First vector generation should not raise exceptions"):
            vectors1 = list(self.operator.run(video))

        # Second generation
        with self.assertNoException("Second vector generation should not raise exceptions"):
            vectors2 = list(self.operator.run(video))

        # Check that we got the same number of vectors each time
        self.assertEqual(len(vectors1), len(vectors2), "Number of vectors should be consistent")

        # Check that the average vectors are identical
        np.testing.assert_array_equal(
            vectors1[0]["vid_vec"],
            vectors2[0]["vid_vec"],
            "Average vectors should be identical for the same video"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests are complete.

        This method is called once after all tests in the class have run.
        It removes the temporary configuration file.
        """
        try:
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
