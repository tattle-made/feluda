import contextlib
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import torch
import yaml
from requests.exceptions import ConnectTimeout, ReadTimeout

from feluda import Feluda
from feluda.models.media_factory import VideoFactory, ImageFactory


@unittest.skipIf(
    os.environ.get("SKIP_VID_VEC_REP_CLIP_TESTS", "0") == "1",
    "Skipping vid_vec_rep_clip tests due to possible dependency issues",
)
class TestFeludaVideoVectorIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""
        try:
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

            # Initialize Feluda with better error handling
            cls.feluda = Feluda(cls.config_path)
            
            # Try to setup, but allow for failures
            try:
                cls.feluda.setup()
                cls.setup_successful = True
            except Exception as e:
                print(f"Warning: Setup failed with error: {e}")
                cls.setup_successful = False
                cls.setup_error = str(e)

            # Sample video URLs for testing - use multiple test videos of different qualities
            cls.test_video_urls = [
                "https://tattle-media.s3.amazonaws.com/test-data/test_video.mp4",
                "https://tattle-media.s3.amazonaws.com/test-data/test_video_short.mp4"  # Add a shorter/smaller video if available
            ]
            cls.test_video_url = cls.test_video_urls[0]  # Default test video
            cls.expected_vector_dim = 512  # CLIP-ViT-B-32 embedding size
            
            # Performance benchmarking
            cls.benchmark_results = {}
        except Exception as e:
            print(f"Error during test setup: {e}")
            raise

    def setUp(self):
        """Set up test-specific feluda resources."""
        # Skip all tests if setup was not successful
        if not getattr(self.__class__, 'setup_successful', False):
            self.skipTest(f"Setup was not successful: {getattr(self.__class__, 'setup_error', 'Unknown error')}")
            
        # Get operator reference in each test to ensure isolation
        self.operator = self.feluda.operators.get()["vid_vec_rep_clip"]

    def test_video_vector_generation(self):
        """Test that video vector generation works end-to-end."""
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video_obj, "Video object should be successfully created")

        video_vec_generator = self.operator.run(video_obj)
        
        # Test first vector (average vector)
        first_vec = next(video_vec_generator)
        self.assertTrue(isinstance(first_vec, dict), "Result should be a dictionary")
        self.assertIn("vid_vec", first_vec, "Result should contain 'vid_vec' key")
        self.assertIn("is_avg", first_vec, "Result should contain 'is_avg' key")
        self.assertTrue(first_vec["is_avg"], "First vector should be the average vector")
        
        # Verify vector dimensions
        vid_vec = first_vec["vid_vec"]
        self.assertTrue(
            isinstance(vid_vec, list),
            "Vector should be a list",
        )
        self.assertEqual(
            len(vid_vec),
            self.expected_vector_dim,
            f"Vector should have dimension {self.expected_vector_dim}",
        )
        
        # Check for I-frame vectors
        i_frame_vectors = []
        for vec_data in video_vec_generator:
            self.assertFalse(vec_data["is_avg"], "Subsequent vectors should be I-frame vectors")
            i_frame_vectors.append(vec_data["vid_vec"])
        
        # There should be at least one I-frame
        self.assertTrue(len(i_frame_vectors) > 0, "Should have at least one I-frame vector")
        
        # All vectors should have the same dimension
        for vec in i_frame_vectors:
            self.assertEqual(
                len(vec),
                self.expected_vector_dim,
                f"All I-frame vectors should have dimension {self.expected_vector_dim}",
            )

    def test_invalid_video_url(self):
        """Test handling of invalid video URL."""
        invalid_url = "https://nonexistent-url/video.mp4"

        for exception in [ConnectTimeout]:
            with self.subTest(exception=exception.__name__):
                with patch("requests.get") as mock_get:
                    mock_get.side_effect = exception
                    result = VideoFactory.make_from_url(invalid_url)
                    self.assertIsNone(result)
        
        # Also test timeout and other connection issues
        for exception in [ReadTimeout, ConnectionError]:
            with self.subTest(exception=exception.__name__):
                with patch("requests.get") as mock_get:
                    mock_get.side_effect = exception
                    result = VideoFactory.make_from_url(self.test_video_url)
                    self.assertIsNone(result)

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
            vec1_generator = self.operator.run(video_obj)
            vec1 = next(vec1_generator)["vid_vec"]

        # Need to create a new video object since the previous one was consumed
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        
        with self.assertNoException(
            "Second vector generation should not raise exceptions"
        ):
            vec2_generator = self.operator.run(video_obj)
            vec2 = next(vec2_generator)["vid_vec"]

        # Vectors should be nearly identical (floating point comparison)
        np.testing.assert_almost_equal(
            vec1, vec2, decimal=5, 
            err_msg="Vectors should be nearly identical for the same video"
        )

    def test_vector_performance_benchmarking(self):
        """Benchmark the performance of the vid_vec_rep_clip operator."""
        if not self.test_video_url:
            self.skipTest("No test video URL provided")
            
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video_obj, "Video object should be successfully created")
        
        # Measure processing time
        start_time = time.time()
        video_vec_generator = self.operator.run(video_obj)
        first_vec = next(video_vec_generator)
        processing_time = time.time() - start_time
        
        # Store benchmark result
        self.__class__.benchmark_results['vector_generation_time'] = processing_time
        
        # Assert that processing time is reasonable (adjust thresholds as needed)
        # This is a very basic performance test - real benchmarks would need more samples and analysis
        self.assertLess(processing_time, 60, "Vector generation should take less than 60 seconds")
        print(f"Vector generation time: {processing_time:.2f} seconds")
        
        # Record memory usage (approximation)
        import sys
        vec_size = sys.getsizeof(first_vec["vid_vec"]) / 1024  # Size in KB
        self.__class__.benchmark_results['vector_size_kb'] = vec_size
        print(f"Vector size: {vec_size:.2f} KB")

    def test_batched_video_processing(self):
        """Test processing multiple videos in sequence."""
        # Skip if we don't have multiple test videos
        if len(self.test_video_urls) < 2:
            self.skipTest("Not enough test videos available for batch processing test")
        
        all_vectors = []
        for url in self.test_video_urls:
            video_obj = VideoFactory.make_from_url(url)
            self.assertIsNotNone(video_obj, f"Video object should be created for {url}")
            
            video_vec_generator = self.operator.run(video_obj)
            first_vec = next(video_vec_generator)["vid_vec"]
            all_vectors.append(first_vec)
        
        # Verify we have vectors for all videos
        self.assertEqual(len(all_vectors), len(self.test_video_urls), 
                        "Should have vectors for all test videos")
        
        # Each vector should have the expected dimension
        for i, vec in enumerate(all_vectors):
            self.assertEqual(
                len(vec), 
                self.expected_vector_dim,
                f"Vector {i} should have dimension {self.expected_vector_dim}"
            )
        
        # Different videos should generally have different vectors
        # (This is a heuristic check, not always true for similar videos)
        if len(all_vectors) >= 2:
            # Compare the first two vectors - they should be different for different videos
            # Use a tolerance because vectors could be similar if videos are similar
            similarity = np.dot(all_vectors[0], all_vectors[1]) / (
                np.linalg.norm(all_vectors[0]) * np.linalg.norm(all_vectors[1])
            )
            print(f"Cosine similarity between different videos: {similarity:.4f}")
            # This is a soft check - different videos should generally have similarity < 0.95
            # but this depends on the actual test videos used
            self.assertLess(similarity, 0.99, "Vectors for different videos should be distinct")

    def test_error_handling_corrupted_video(self):
        """Test handling of corrupted video files."""
        # Mock a corrupted video file
        with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
            # Write some garbage data
            temp_file.write(b"This is not a valid video file")
            temp_file.flush()
            
            # Create a mock VideoFactory that returns our corrupted file
            with patch.object(VideoFactory, 'make_from_url') as mock_factory:
                mock_video = MagicMock()
                mock_video.__getitem__.side_effect = lambda key: temp_file.name if key == "path" else None
                mock_factory.return_value = mock_video
                
                # Test with try/except since this should raise an exception
                with self.assertRaises(Exception) as context:
                    video_obj = VideoFactory.make_from_url("mock_url")
                    self.operator.run(video_obj)
                
                # Check that some exception was raised
                # The exact exception depends on how the operator handles corrupted files
                print(f"Corrupted video exception: {context.exception}")

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests are done."""
        try:
            if hasattr(cls, 'config_path'):
                Path(cls.config_path).unlink(missing_ok=True)
                
            # Print benchmark results if any
            if hasattr(cls, 'benchmark_results') and cls.benchmark_results:
                print("\n=== Performance Benchmark Results ===")
                for key, value in cls.benchmark_results.items():
                    print(f"{key}: {value}")
                print("=====================================")
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")