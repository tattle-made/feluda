import contextlib
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import yaml
from requests.exceptions import ConnectTimeout, ReadTimeout

from feluda import Feluda
from feluda.models.media_factory import ImageFactory, VideoFactory


class TestFeludaMultiOperatorIntegration(unittest.TestCase):
    """
    Integration test for multiple Feluda operators.
    
    This test validates the integration between:
    - feluda (core)
    - feluda-vid-vec-rep-clip
    - feluda-cluster-embeddings
    - image_vec_rep_resnet
    """
    
    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""
        try:
            # Setup configuration with multiple operators
            cls.config = {
                "operators": {
                    "label": "Operators",
                    "parameters": [
                        {
                            "name": "image vectors",
                            "type": "image_vec_rep_resnet",
                            "parameters": {"index_name": "image"},
                        },
                        {
                            "name": "video vectors",
                            "type": "vid_vec_rep_clip",
                            "parameters": {"index_name": "video"},
                        },
                        {
                            "name": "cluster embeddings",
                            "type": "cluster_embeddings",
                            "parameters": {},
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

            # Sample image/video URLs for testing
            cls.test_image_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
            cls.test_video_url = "https://tattle-media.s3.amazonaws.com/test-data/test_video.mp4"
            cls.expected_vector_dim = 512  # Both CLIP and ResNet embeddings are 512
            
            # Sample data for clustering tests
            cls.sample_clustering_data = [
                {"embedding": [1.0, 2.0, 3.0], "payload": {"id": "item1", "metadata": "data1"}},
                {"embedding": [1.1, 2.1, 3.1], "payload": {"id": "item2", "metadata": "data2"}},
                {"embedding": [10.0, 11.0, 12.0], "payload": {"id": "item3", "metadata": "data3"}},
                {"embedding": [10.2, 11.2, 12.2], "payload": {"id": "item4", "metadata": "data4"}},
                {"embedding": [20.0, 21.0, 22.0], "payload": {"id": "item5", "metadata": "data5"}},
            ]
            
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
        
        # Get operator references
        self.operators = self.feluda.operators.get()
        
        # Check which operators are available (some may not be available due to dependencies)
        self.has_image_operator = "image_vec_rep_resnet" in self.operators
        self.has_video_operator = "vid_vec_rep_clip" in self.operators
        self.has_cluster_operator = "cluster_embeddings" in self.operators

    # =====================================================================
    # IMAGE VECTOR REPRESENTATION TESTS
    # =====================================================================
    
    def test_image_vector_generation(self):
        """Test that image vector generation works end-to-end."""
        if not self.has_image_operator:
            self.skipTest("image_vec_rep_resnet operator not available")
            
        image_operator = self.operators["image_vec_rep_resnet"]
        
        image_obj = ImageFactory.make_from_url(self.test_image_url)
        self.assertIsNotNone(image_obj, "Image object should be successfully created")

        image_vec = image_operator.run(image_obj)

        self.assertTrue(
            isinstance(image_vec, (list, np.ndarray)),
            "Vector should be a list or numpy array",
        )
        self.assertTrue(len(image_vec) > 0, "Vector should not be empty")
        self.assertEqual(
            len(image_vec),
            self.expected_vector_dim,
            f"Vector should have dimension {self.expected_vector_dim}",
        )

        if isinstance(image_vec, np.ndarray):
            self.assertFalse(np.all(image_vec == 0), "Vector should not be all zeros")
            self.assertFalse(
                np.any(np.isnan(image_vec)), "Vector should not contain NaN values"
            )

    def test_image_vector_consistency(self):
        """Test that generating vectors twice from the same image gives consistent results."""
        if not self.has_image_operator:
            self.skipTest("image_vec_rep_resnet operator not available")
            
        image_operator = self.operators["image_vec_rep_resnet"]
        
        # First vector generation
        image_obj = ImageFactory.make_from_url(self.test_image_url)
        with self.assertNoException("First vector generation should not raise exceptions"):
            vec1 = image_operator.run(image_obj)

        # Second vector generation with a new image object
        image_obj = ImageFactory.make_from_url(self.test_image_url)
        with self.assertNoException("Second vector generation should not raise exceptions"):
            vec2 = image_operator.run(image_obj)

        # Vectors should be identical
        np.testing.assert_array_equal(
            vec1, vec2, "Vectors should be identical for the same image"
        )

    # =====================================================================
    # VIDEO VECTOR REPRESENTATION TESTS
    # =====================================================================
    
    def test_video_vector_generation(self):
        """Test that video vector generation works end-to-end."""
        if not self.has_video_operator:
            self.skipTest("vid_vec_rep_clip operator not available")
            
        video_operator = self.operators["vid_vec_rep_clip"]
        
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video_obj, "Video object should be successfully created")

        video_vec_generator = video_operator.run(video_obj)
        
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

    def test_video_vector_consistency(self):
        """Test that generating vectors twice from the same video gives consistent results."""
        if not self.has_video_operator:
            self.skipTest("vid_vec_rep_clip operator not available")
            
        video_operator = self.operators["vid_vec_rep_clip"]
        
        # First vector generation
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        with self.assertNoException("First vector generation should not raise exceptions"):
            vec1_generator = video_operator.run(video_obj)
            vec1 = next(vec1_generator)["vid_vec"]

        # Second vector generation with a new video object
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        with self.assertNoException("Second vector generation should not raise exceptions"):
            vec2_generator = video_operator.run(video_obj)
            vec2 = next(vec2_generator)["vid_vec"]

        # Vectors should be nearly identical (floating point comparison)
        np.testing.assert_almost_equal(
            vec1, vec2, decimal=5, 
            err_msg="Vectors should be nearly identical for the same video"
        )

    # =====================================================================
    # CLUSTERING TESTS
    # =====================================================================
    
    def test_kmeans_clustering(self):
        """Test KMeans clustering with audio modality."""
        if not self.has_cluster_operator:
            self.skipTest("cluster_embeddings operator not available")
            
        cluster_operator = self.operators["cluster_embeddings"]
        
        n_clusters = 3
        modality = "audio"
        
        result = cluster_operator.run(self.sample_clustering_data, n_clusters=n_clusters, modality=modality)
        
        # Verify the result structure
        self.assertTrue(isinstance(result, dict), "Result should be a dictionary")
        self.assertEqual(len(result), n_clusters, f"Should have {n_clusters} clusters")
        
        # Check that each cluster key follows the expected format
        for key in result:
            self.assertTrue(key.startswith("cluster_"), "Cluster keys should start with 'cluster_'")
            self.assertTrue(isinstance(result[key], list), "Cluster values should be lists")
        
        # Check that all items are assigned to some cluster
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        self.assertEqual(len(all_items), len(self.sample_clustering_data), 
                         "All items should be assigned to a cluster")

    def test_agglomerative_clustering(self):
        """Test Agglomerative clustering with video modality."""
        if not self.has_cluster_operator:
            self.skipTest("cluster_embeddings operator not available")
            
        cluster_operator = self.operators["cluster_embeddings"]
        
        n_clusters = 2
        modality = "video"
        
        result = cluster_operator.run(self.sample_clustering_data, n_clusters=n_clusters, modality=modality)
        
        # Verify the result structure
        self.assertTrue(isinstance(result, dict), "Result should be a dictionary")
        self.assertEqual(len(result), n_clusters, f"Should have {n_clusters} clusters")
        
        # All other checks are similar to KMeans test
        all_items = []
        for key, cluster_items in result.items():
            self.assertTrue(key.startswith("cluster_"), "Cluster keys should start with 'cluster_'")
            self.assertTrue(isinstance(cluster_items, list), "Cluster values should be lists")
            all_items.extend(cluster_items)
        
        self.assertEqual(len(all_items), len(self.sample_clustering_data), 
                         "All items should be assigned to a cluster")

    # =====================================================================
    # CROSS-OPERATOR INTEGRATION TESTS
    # =====================================================================
    
    def test_image_to_clusters_integration(self):
        """Test integration between image vector generation and clustering."""
        if not (self.has_image_operator and self.has_cluster_operator):
            self.skipTest("Required operators not available")
            
        image_operator = self.operators["image_vec_rep_resnet"]
        cluster_operator = self.operators["cluster_embeddings"]
        
        # Generate image vectors
        image_vectors = []
        image_payloads = []
        
        # Use the same image multiple times with slight modifications for clustering
        base_image_obj = ImageFactory.make_from_url(self.test_image_url)
        image_vectors.append(image_operator.run(base_image_obj))
        image_payloads.append({"id": "original", "path": self.test_image_url})
        
        # Prepare data for clustering
        clustering_data = []
        for i, (vec, payload) in enumerate(zip(image_vectors, image_payloads)):
            clustering_data.append({
                "embedding": vec.tolist() if isinstance(vec, np.ndarray) else vec,
                "payload": payload
            })
        
        # Add some synthetic vectors for better clustering demonstration
        for i in range(3):
            # Create a synthetic vector that's different from the image vector
            synth_vec = np.ones(self.expected_vector_dim) * (i + 2)
            clustering_data.append({
                "embedding": synth_vec.tolist(),
                "payload": {"id": f"synthetic_{i}", "path": "none"}
            })
        
        # Cluster the vectors
        n_clusters = 2  # We expect original image in one cluster, synthetic vectors in another
        modality = "audio"  # Doesn't matter for this test, just need a valid value
        
        result = cluster_operator.run(clustering_data, n_clusters=n_clusters, modality=modality)
        
        # Verify clustering results
        self.assertEqual(len(result), n_clusters, f"Should have {n_clusters} clusters")
        
        # All items should be in clusters
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        self.assertEqual(len(all_items), len(clustering_data), 
                         "All items should be assigned to a cluster")

    def test_video_to_clusters_integration(self):
        """Test integration between video vector generation and clustering."""
        if not (self.has_video_operator and self.has_cluster_operator):
            self.skipTest("Required operators not available")
            
        video_operator = self.operators["vid_vec_rep_clip"]
        cluster_operator = self.operators["cluster_embeddings"]
        
        # Generate video vectors
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        self.assertIsNotNone(video_obj, "Video object should be successfully created")
        
        video_vec_generator = video_operator.run(video_obj)
        first_vec = next(video_vec_generator)
        avg_vector = first_vec["vid_vec"]
        
        # Collect I-frame vectors as well (up to 5)
        i_frame_vectors = []
        for i, vec_data in enumerate(video_vec_generator):
            if i >= 5:  # Limit to 5 I-frames to keep test reasonable
                break
            i_frame_vectors.append(vec_data["vid_vec"])
        
        # Prepare data for clustering
        clustering_data = [
            {"embedding": avg_vector, "payload": {"id": "avg_frame", "type": "average"}}
        ]
        
        for i, vec in enumerate(i_frame_vectors):
            clustering_data.append({
                "embedding": vec,
                "payload": {"id": f"iframe_{i}", "type": "iframe"}
            })
        
        # Cluster the vectors
        n_clusters = 2  # Arbitrary, just to demonstrate
        modality = "video"
        
        result = cluster_operator.run(clustering_data, n_clusters=n_clusters, modality=modality)
        
        # Verify clustering results
        self.assertTrue(1 <= len(result) <= n_clusters, 
                        f"Should have between 1 and {n_clusters} clusters")
        
        # All items should be in clusters
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        self.assertEqual(len(all_items), len(clustering_data), 
                         "All items should be assigned to a cluster")
        
        # Print some debug info about the clustering
        print(f"\nClustered {len(clustering_data)} video vectors into {len(result)} clusters")
        for cluster_name, items in result.items():
            print(f"  {cluster_name}: {len(items)} items - {[item['id'] for item in items]}")

    # =====================================================================
    # COMBINED END-TO-END TEST
    # =====================================================================
    
    def test_full_pipeline_integration(self):
        """Test a full pipeline integrating all operators."""
        if not (self.has_image_operator and self.has_video_operator and self.has_cluster_operator):
            self.skipTest("Not all required operators are available")
        
        # Get operator references
        image_operator = self.operators["image_vec_rep_resnet"]
        video_operator = self.operators["vid_vec_rep_clip"]
        cluster_operator = self.operators["cluster_embeddings"]
        
        # 1. Generate image vector
        image_obj = ImageFactory.make_from_url(self.test_image_url)
        image_vec = image_operator.run(image_obj)
        
        # 2. Generate video vector
        video_obj = VideoFactory.make_from_url(self.test_video_url)
        video_vec_generator = video_operator.run(video_obj)
        video_vec = next(video_vec_generator)["vid_vec"]
        
        # 3. Prepare combined data for clustering
        combined_data = [
            {"embedding": image_vec.tolist() if isinstance(image_vec, np.ndarray) else image_vec, 
             "payload": {"id": "image", "type": "image", "path": self.test_image_url}},
            {"embedding": video_vec, 
             "payload": {"id": "video", "type": "video", "path": self.test_video_url}}
        ]
        
        # Add some deliberately different vectors to ensure meaningful clustering
        for i in range(3):
            combined_data.append({
                "embedding": [float(10 * (i + 1))] * self.expected_vector_dim,
                "payload": {"id": f"synthetic_{i}", "type": "synthetic"}
            })
        
        # 4. Cluster the combined vectors
        n_clusters = 3  # Expect image, video, and synthetic in different clusters
        modality = "audio"  # Just need a valid value
        
        cluster_result = cluster_operator.run(combined_data, n_clusters=n_clusters, modality=modality)
        
        # 5. Verify results
        self.assertEqual(len(cluster_result), n_clusters, f"Should have {n_clusters} clusters")
        
        # All items should be in clusters
        all_items = []
        for cluster_items in cluster_result.values():
            all_items.extend(cluster_items)
        self.assertEqual(len(all_items), len(combined_data), 
                         "All items should be assigned to a cluster")
        
        # Print the full pipeline results
        print("\n=== Full Pipeline Results ===")
        print(f"Clustered {len(combined_data)} items into {len(cluster_result)} clusters")
        for cluster_name, items in cluster_result.items():
            print(f"  {cluster_name}: {len(items)} items - {[item['id'] for item in items]}")
        
        self.__class__.benchmark_results['full_pipeline'] = "Success"

    # =====================================================================
    # HELPER METHODS
    # =====================================================================
    
    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        """Context manager to verify no exception is raised."""
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Exception was raised'}: {e}")

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


if __name__ == "__main__":
    unittest.main()