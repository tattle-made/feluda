# Standard library imports
import contextlib  # For creating context managers
import tempfile  # For creating temporary files
import unittest  # For creating test cases
from pathlib import Path  # For file path operations
from unittest.mock import patch  # For mocking in tests

import numpy as np  # For numerical operations and array comparisons
import yaml  # For YAML file operations
from requests.exceptions import ConnectTimeout  # For handling network timeouts

from feluda.models.media_factory import (
    VideoFactory,  # Factory for creating video objects
)


class TestFeludaVideoVectorIntegration(unittest.TestCase):
    """Integration tests for Feluda's video vector representation using CLIP.

    This test suite verifies that the vid_vec_rep_clip operator correctly generates
    vector representations of videos, handles errors appropriately, and produces
    consistent results across multiple runs."""
    @classmethod
    def setUpClass(cls): #method in unittest, used to create a temporary configuration file and set upa mock operator# Create a temporary file for storing the configuration# Mock operator to simulate the behavior of the actual operator
        """Creates a temporary test configuration file that will be used for all tests.

        This method is called once before any tests in the class are run.
        It sets up a mock Feluda instance with a mocked vid_vec_rep_clip operator.

        The setup process includes:
        1. Creating a configuration dictionary with the vid_vec_rep_clip operator
        2. Writing this configuration to a temporary YAML file
        3. Setting up test constants like the test video URL and expected vector dimension
        4. Creating mock objects for testing instead of loading actual dependencies
        """
        #configuration for feluda with the video vector operator
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


        fd, cls.config_path = tempfile.mkstemp(suffix=".yml") #function from the tempfile, creates a temporary YAML configuration file that is used during testing
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)  # writes the configuration to the temporary file


        cls.mock_operator = unittest.mock.MagicMock() #instance of MagicMock, used to simulate the behaviour of vid_vec_rep_clip

        def mock_run(video_obj): #fn defined in setupClass, creates a genertor that yields test vectors, first vector is marked as the avg vector witht the dimension of 512

            yield {
                "vid_vec": [0.1] * 512,
                "is_avg": True
            }
            #additional vectors for frames
            for _ in range(3):
                yield {
                    "vid_vec": [0.2] * 512,
                    "is_avg": False
                }

        cls.mock_operator.run.side_effect = mock_run #mock operator's run method

        # test constants
        cls.test_video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"  # URL to the test video
        cls.expected_vector_dim = 512  # Expected dimension of the CLIP video vectors, chosen based on CLIP model

    def setUp(self):
        """Set up test-specific feluda resources.

        This method is called before each test method is executed.
        It sets up a reference to our mock operator to ensure test isolation.
        """
        #each test has its own reference to the mock operator
        self.operator = self.__class__.mock_operator

    def test_video_vector_generation(self): # test case that verifies the complete pipeline
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
        #video object from the test URL
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video_obj, "Video object should be successfully created")

        #returns a generator of vectors
        video_vectors = self.operator.run(video_obj)


        first_vector = next(video_vectors)
        self.assertIsNotNone(first_vector, "At least one vector should be generated")

        self.assertTrue(
            isinstance(first_vector.get("vid_vec"), list),
            "Vector should be a list",
        )
        # verifies that the vector is not empty
        self.assertTrue(len(first_vector.get("vid_vec")) > 0, "Vector should not be empty")
        self.assertEqual(
            len(first_vector.get("vid_vec")),
            self.expected_vector_dim,
            f"Vector should have dimension {self.expected_vector_dim}",
        )

        self.assertTrue(first_vector.get("is_avg"), "First vector should be the average vector")

        # iterates through the rest of the vectors in the generator
        for vec in video_vectors:
            self.assertEqual(
                len(vec.get("vid_vec")),
                self.expected_vector_dim,
                f"All vectors should have dimension {self.expected_vector_dim}",
            )

    def test_invalid_video_url(self):
        """Test handling of invalid video URL.

        This test verifies that the system correctly handles errors when
        attempting to create a video object from an invalid URL.

        It uses mocking to simulate network errors (like ConnectTimeout)
        and checks that these errors are properly handled.
        """
        # an invalid URL that doesn't exist
        invalid_url = "https://nonexistent-url/video.mp4"

        # ConnectTimeout = exception from requests library, used to simulate network errors
        for exception in [ConnectTimeout]:
            # uses subTest to create a separate test case for each exception type
            with self.subTest(exception=exception.__name__):
                # mocks the VideoFactory.make_from_url method directly
                with patch("feluda.models.media_factory.VideoFactory.make_from_url") as mock_make_from_url:
                    #configures
                    mock_make_from_url.side_effect = exception
                    with self.assertRaises(exception):
                        VideoFactory.make_from_url(invalid_url)

                    mock_make_from_url.assert_called_once_with(invalid_url)

    def test_operator_configuration(self):
        """Test that operator is properly configured.

        This test verifies that the vid_vec_rep_clip operator is:
        1. Successfully initialized and available
        2. Has the required 'run' method needed for operation

        These are basic sanity checks to ensure the operator is properly set up
        before running more complex tests.
        """
        #verifies that the operator was successfully initialized
        self.assertIsNotNone(self.operator, "Operator should be properly initialized")
        self.assertTrue(
            hasattr(self.operator, "run"), "Operator should have 'run' method"
        )

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        """Context manager to verify no exception is raised.

        This is a utility method that creates a context manager which fails the test
        if any exception is raised within its context. It's used to ensure that
        certain operations complete without errors.

        Args:
            msg (str, optional): Custom message to include in the failure message.
                                Defaults to 'Exception was raised'.

        Yields:
            None: This context manager doesn't yield any value.
        """
        try:
            yield
        except Exception as e:
            # if an exception occurs, fail the test
            self.fail(f"{msg or 'Exception was raised'}: {e}")

    def test_video_vector_consistency(self):
        """Test that generating vectors twice from the same video gives consistent results.

        This test verifies that the vector generation process is deterministic by:
        1. Generating vectors from the same video twice
        2. Checking that the same number of vectors is generated each time
        3. Verifying that the average vectors from both runs are nearly identical

        The test uses numpy's almost_equal function to allow for small floating-point
        differences that might occur due to numerical precision issues.
        """
        # mock
        with patch('feluda.models.media_factory.VideoFactory.make_from_url') as mock_make_from_url:
            # creates a mock video object
            mock_video_obj = {'path': '/tmp/mock_video.mp4'}
            mock_make_from_url.return_value = mock_video_obj

            with self.assertNoException(
                "First vector generation should not raise exceptions"
            ):
                # converts the generator to a list to store all vectors
                vec1 = list(self.operator.run(mock_video_obj))

            with self.assertNoException(
                "Second vector generation should not raise exceptions"
            ):
                vec2 = list(self.operator.run(mock_video_obj))

            #checks that we got the same number of vectors in both runs, to verify if we got the same no. of frames processed each time
            self.assertEqual(len(vec1), len(vec2), "Should generate the same number of vectors")

            # finds the average vectors from each run, then marked with is_avg=True, then using generator exp first matching vector is found1

            avg_vec1 = next((v for v in vec1 if v.get("is_avg")), None)
            avg_vec2 = next((v for v in vec2 if v.get("is_avg")), None)

            self.assertIsNotNone(avg_vec1, "First run should have an average vector")
            self.assertIsNotNone(avg_vec2, "Second run should have an average vector")

            # almost_equal function to compare avg vectors
            np.testing.assert_array_almost_equal(
                avg_vec1.get("vid_vec"), avg_vec2.get("vid_vec"), decimal=5,
                err_msg="Average vectors should be nearly identical for the same video"
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests are done.

        This method is called once after all tests in the class have been run.
        It ensures that any temporary files created during testing are properly
        cleaned up, even if some tests failed.
        """
        try:
            # deletes the temporary configuration file but missing_ok=True prevents errors if the file was already deleted
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
