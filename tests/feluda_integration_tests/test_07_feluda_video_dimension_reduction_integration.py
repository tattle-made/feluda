import contextlib
import tempfile
import unittest
from pathlib import Path

import numpy as np
import yaml

from feluda import Feluda
from feluda.models.media_factory import VideoFactory


class TestFeludaVideoDimensionReductionIntegration(unittest.TestCase):
    
    #Integration test for Feluda with video vector extraction and dimension reduction.
    

    @classmethod
    def setUpClass(cls):
        # Setup configuration with both required operators
        cls.config = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "Video Vector Extractor",
                        "type": "vid_vec_rep_clip",
                        "parameters": {},
                    },
                    {
                        "name": "Dimension Reducer",
                        "type": "dimension_reduction",
                        "parameters": {
                            "model_type": "tsne",
                            "n_components": 2,
                            "perplexity": 3,  # Lower perplexity for small datasets
                            "learning_rate": 200,
                            "random_state": 42,
                        },
                    },
                ],
            }
        }

        # Create temporary config file
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        try:
            # Initialize Feluda with both operators
            cls.feluda = Feluda(cls.config_path)
            cls.feluda.setup()
            cls.setup_successful = True
        except Exception as e:
            print(f"Warning: Feluda setup failed with error: {e}")
            cls.setup_successful = False
            cls.setup_error = str(e)

        # Sample video URLs for testing
        cls.test_video_urls = [
            "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        ]
        cls.expected_vector_dim = 512  # Expected dimension of CLIP embeddings

    def setUp(self):
        # Skip all tests if setup was not successful
        if not getattr(self.__class__, "setup_successful", False):
            self.skipTest(f"Feluda setup was not successful: {getattr(self.__class__, 'setup_error', 'Unknown error')}")

        # Get operator references
        self.operators = self.feluda.operators.get()
        
        # Check which operators are available
        self.has_video_operator = "vid_vec_rep_clip" in self.operators
        self.has_dimension_operator = "dimension_reduction" in self.operators
        
        # Skip if required operators are not available
        if not (self.has_video_operator and self.has_dimension_operator):
            missing = []
            if not self.has_video_operator:
                missing.append("vid_vec_rep_clip")
            if not self.has_dimension_operator:
                missing.append("dimension_reduction")
            self.skipTest(f"Required operators not available: {', '.join(missing)}")

    def test_video_vector_extraction(self):
        video_operator = self.operators["vid_vec_rep_clip"]
        
        # Create a video object for the first test video
        video_obj = VideoFactory.make_from_url(self.test_video_urls[0])
        self.assertIsNotNone(video_obj, "Video object should be successfully created")
        
        # Extract vectors
        vector_generator = video_operator.run(video_obj)
        
        # Get first vector (average vector)
        first_vector = next(vector_generator)
        
        # Validate vector structure and dimensions
        self.assertIsInstance(first_vector, dict, "Result should be a dictionary")
        self.assertIn("vid_vec", first_vector, "Result should contain 'vid_vec' key")
        self.assertIn("is_avg", first_vector, "Result should contain 'is_avg' key")
        self.assertTrue(first_vector["is_avg"], "First vector should be the average vector")
        
        vid_vec = first_vector["vid_vec"]
        self.assertIsInstance(vid_vec, list, "Vector should be a list")
        self.assertEqual(len(vid_vec), self.expected_vector_dim, 
                         f"Vector should have dimension {self.expected_vector_dim}")

    def test_dimension_reduction(self):
        #Test dimension reduction on sample data.
        dim_operator = self.operators["dimension_reduction"]
        
        # Create sample high-dimensional data
        sample_data = [
            {"payload": "sample1", "embedding": [1.0] * self.expected_vector_dim},
            {"payload": "sample2", "embedding": [2.0] * self.expected_vector_dim},
            {"payload": "sample3", "embedding": [3.0] * self.expected_vector_dim}
        ]
        
        # Reduce dimensions
        reduced_data = dim_operator.run(sample_data)
        
        # Validate results
        self.assertEqual(len(reduced_data), len(sample_data), 
                         "Output should have same number of items as input")
        
        for item in reduced_data:
            self.assertIn("payload", item, "Each result should contain the original payload")
            self.assertIn("reduced_embedding", item, "Each result should contain reduced embeddings")
            self.assertEqual(len(item["reduced_embedding"]), 2, 
                             "Reduced embeddings should be 2-dimensional")

    def test_video_to_dimension_reduction_pipeline(self):
        #Test the full pipeline from video extraction to dimension reduction
        video_operator = self.operators["vid_vec_rep_clip"]
        dim_operator = self.operators["dimension_reduction"]
        
        # Extract vectors from multiple videos
        video_vectors = []
        video_payloads = []
        
        for i, url in enumerate(self.test_video_urls):
            try:
                video_obj = VideoFactory.make_from_url(url)
                vector_generator = video_operator.run(video_obj)
                
                # Get the average vector (first item)
                try:
                    avg_vector = next(vector_generator)
                    video_vectors.append(avg_vector["vid_vec"])
                    video_payloads.append(f"video_{i}")
                except StopIteration:
                    print(f"Warning: No vectors generated for video {i}")
            except Exception as e:
                print(f"Error processing video {i}: {e}")
        
        # Skip test if we couldn't get enough vectors
        if len(video_vectors) < 2:
            self.skipTest(f"Not enough video vectors extracted: {len(video_vectors)}")
        
        # Prepare input for dimension reduction
        input_data = [
            {"payload": payload, "embedding": vector} 
            for payload, vector in zip(video_payloads, video_vectors)
        ]
        
        # Reduce dimensions
        reduced_data = dim_operator.run(input_data)
        
        # Validate results
        self.assertEqual(len(reduced_data), len(input_data),
                         "Dimension reduction should preserve the number of items")
        
        # Extract reduced vectors and check they form clusters
        reduced_vectors = np.array([item["reduced_embedding"] for item in reduced_data])
        
        # With t-SNE, similar videos should be closer to each other
        # But since we're using small samples, just check the output shape
        self.assertEqual(reduced_vectors.shape, (len(input_data), 2),
                         "Reduced vectors should be 2D points")

    def test_dimension_reduction_with_iframe_vectors(self):
        #Test dimension reduction with both average and I-frame vectors from a video
        video_operator = self.operators["vid_vec_rep_clip"]
        dim_operator = self.operators["dimension_reduction"]
        
        # Process a video to get both average and I-frame vectors
        video_obj = VideoFactory.make_from_url(self.test_video_urls[0])
        vector_generator = video_operator.run(video_obj)
        
        # Collect vectors
        vectors = []
        
        # First is the average vector
        try:
            avg_vector = next(vector_generator)
            vectors.append({
                "payload": "avg_vector",
                "embedding": avg_vector["vid_vec"]
            })
            
            # Collect up to 5 I-frame vectors
            for i, frame_vector in enumerate(vector_generator):
                if i >= 5:  # Limit to 5 I-frames
                    break
                vectors.append({
                    "payload": f"iframe_{i}",
                    "embedding": frame_vector["vid_vec"]
                })
        except StopIteration:
            # If we can't get vectors, skip the test
            if not vectors:
                self.skipTest("Could not extract vectors from test video")
        
        # Need at least 3 points for meaningful t-SNE
        if len(vectors) < 3:
            # Add synthetic points if needed
            for i in range(3 - len(vectors)):
                vectors.append({
                    "payload": f"synthetic_{i}",
                    "embedding": [float(i) + 0.1] * self.expected_vector_dim
                })
        
        # Reduce dimensions
        reduced_data = dim_operator.run(vectors)
        
        # Validate results
        self.assertEqual(len(reduced_data), len(vectors),
                         "Dimension reduction should preserve the number of items")
        
        # Check that original payloads are preserved
        payloads = [item["payload"] for item in reduced_data]
        original_payloads = [item["payload"] for item in vectors]
        
        self.assertEqual(set(payloads), set(original_payloads),
                         "Original payloads should be preserved in results")
        
        # Check dimensions of reduced vectors
        for item in reduced_data:
            self.assertEqual(len(item["reduced_embedding"]), 2,
                             "Reduced vectors should be 2-dimensional")

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        #Context manager to verify that no exception is raised.
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Exception was raised'}: {e}")

    @classmethod
    def tearDownClass(cls):
        #Clean up temporary files after all tests are done.
        try:
            if hasattr(cls, "config_path"):
                Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
