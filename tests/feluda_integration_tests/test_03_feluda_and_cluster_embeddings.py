import contextlib
import os
import tempfile
import time
import unittest
from pathlib import Path

import numpy as np
import yaml
from unittest.mock import patch

from feluda import Feluda


@unittest.skipIf(
    os.environ.get("SKIP_CLUSTER_EMBEDDINGS_TESTS", "0") == "1",
    "Skipping cluster_embeddings tests due to possible dependency issues",
)
class TestFeludaClusterEmbeddingsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""
        try:
            # Setup configuration with just the cluster embeddings operator
            cls.config = {
                "operators": {
                    "label": "Operators",
                    "parameters": [
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

            # Sample data for clustering tests
            # Standard test data
            cls.sample_data = [
                {"embedding": [1.0, 2.0, 3.0], "payload": {"id": "item1", "metadata": "data1"}},
                {"embedding": [1.1, 2.1, 3.1], "payload": {"id": "item2", "metadata": "data2"}},
                {"embedding": [10.0, 11.0, 12.0], "payload": {"id": "item3", "metadata": "data3"}},
                {"embedding": [10.2, 11.2, 12.2], "payload": {"id": "item4", "metadata": "data4"}},
                {"embedding": [20.0, 21.0, 22.0], "payload": {"id": "item5", "metadata": "data5"}},
            ]
            
            # Edge case test data
            cls.large_sample_data = []
            # Generate 100 sample embeddings for stress testing
            for i in range(100):
                # Create clusters with noise
                if i < 30:
                    embedding = [1.0 + np.random.normal(0, 0.1), 
                                2.0 + np.random.normal(0, 0.1), 
                                3.0 + np.random.normal(0, 0.1)]
                elif i < 70:
                    embedding = [10.0 + np.random.normal(0, 0.1), 
                                11.0 + np.random.normal(0, 0.1), 
                                12.0 + np.random.normal(0, 0.1)]
                else:
                    embedding = [20.0 + np.random.normal(0, 0.1), 
                                21.0 + np.random.normal(0, 0.1), 
                                22.0 + np.random.normal(0, 0.1)]
                
                cls.large_sample_data.append({
                    "embedding": embedding,
                    "payload": {"id": f"large_item{i}", "metadata": f"large_data{i}"}
                })
            
            # High-dimensional test data
            cls.high_dim_data = []
            for i in range(20):
                # Create 100-dimensional embeddings
                embedding = [float(j % 10 + np.random.normal(0, 0.1)) for j in range(100)]
                cls.high_dim_data.append({
                    "embedding": embedding,
                    "payload": {"id": f"highdim_item{i}", "metadata": f"highdim_data{i}"}
                })
                
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
        self.operator = self.feluda.operators.get()["cluster_embeddings"]

    def test_kmeans_clustering(self):
        """Test KMeans clustering with audio modality."""
        n_clusters = 3
        modality = "audio"
        
        result = self.operator.run(self.sample_data, n_clusters=n_clusters, modality=modality)
        
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
        self.assertEqual(len(all_items), len(self.sample_data), "All items should be assigned to a cluster")
        
        # Check that similar embeddings are in the same cluster
        similar_pairs = [(0, 1), (2, 3)]  # Indices of similar embeddings
        for i, j in similar_pairs:
            # Find which clusters contain these items
            cluster_i = None
            cluster_j = None
            for cluster, items in result.items():
                if any(item["id"] == self.sample_data[i]["payload"]["id"] for item in items):
                    cluster_i = cluster
                if any(item["id"] == self.sample_data[j]["payload"]["id"] for item in items):
                    cluster_j = cluster
            
            self.assertEqual(cluster_i, cluster_j, 
                             f"Similar embeddings {i} and {j} should be in the same cluster")

    def test_agglomerative_clustering(self):
        """Test Agglomerative clustering with video modality."""
        n_clusters = 2
        modality = "video"
        
        result = self.operator.run(self.sample_data, n_clusters=n_clusters, modality=modality)
        
        # Verify the result structure
        self.assertTrue(isinstance(result, dict), "Result should be a dictionary")
        self.assertEqual(len(result), n_clusters, f"Should have {n_clusters} clusters")
        
        # All other checks are similar to KMeans test
        all_items = []
        for key, cluster_items in result.items():
            self.assertTrue(key.startswith("cluster_"), "Cluster keys should start with 'cluster_'")
            self.assertTrue(isinstance(cluster_items, list), "Cluster values should be lists")
            all_items.extend(cluster_items)
        
        self.assertEqual(len(all_items), len(self.sample_data), "All items should be assigned to a cluster")

    def test_affinity_propagation_clustering(self):
        """Test Affinity Propagation clustering (no n_clusters specified)."""
        # No n_clusters specified, should use AffinityPropagation
        result = self.operator.run(self.sample_data, modality="audio")
        
        # Verify the result structure
        self.assertTrue(isinstance(result, dict), "Result should be a dictionary")
        self.assertTrue(len(result) > 0, "Should have at least one cluster")
        
        # All other checks are similar to previous tests
        all_items = []
        for key, cluster_items in result.items():
            self.assertTrue(key.startswith("cluster_"), "Cluster keys should start with 'cluster_'")
            self.assertTrue(isinstance(cluster_items, list), "Cluster values should be lists")
            all_items.extend(cluster_items)
        
        self.assertEqual(len(all_items), len(self.sample_data), "All items should be assigned to a cluster")

    def test_invalid_modality(self):
        """Test handling of invalid modality."""
        with self.assertRaises(ValueError) as context:
            self.operator.run(self.sample_data, n_clusters=3, modality="invalid")
        
        self.assertIn("Invalid modality", str(context.exception), 
                      "Should raise ValueError with 'Invalid modality' message")

    def test_missing_keys_in_data(self):
        """Test handling of data missing required keys."""
        invalid_data = [
            {"embedding": [1.0, 2.0, 3.0]},  # Missing 'payload'
            {"payload": {"id": "item2"}}      # Missing 'embedding'
        ]
        
        with self.assertRaises(KeyError) as context:
            self.operator.run(invalid_data, n_clusters=2, modality="audio")
        
        self.assertIn("Invalid data", str(context.exception), 
                      "Should raise KeyError with 'Invalid data' message")

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        """Context manager to verify no exception is raised."""
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Exception was raised'}: {e}")

    def test_clustering_consistency(self):
        """Test that clustering the same data twice gives consistent results."""
        n_clusters = 3
        modality = "audio"
        
        with self.assertNoException("First clustering should not raise exceptions"):
            result1 = self.operator.run(self.sample_data, n_clusters=n_clusters, modality=modality)
        
        with self.assertNoException("Second clustering should not raise exceptions"):
            result2 = self.operator.run(self.sample_data, n_clusters=n_clusters, modality=modality)
        
        # Check that the number of clusters is the same
        self.assertEqual(len(result1), len(result2), 
                         "Number of clusters should be the same in both runs")
        
        # Check that the cluster assignments are the same
        # Note: We need to map the actual cluster labels since they might be arbitrary
        cluster_map = {}
        for key1, items1 in result1.items():
            # Find the matching cluster in result2 based on the first item in items1
            for key2, items2 in result2.items():
                if items2[0]["id"] == items1[0]["id"]:
                    cluster_map[key1] = key2
                    break
        
        # Verify that all items are in the same relative clusters
        for key1, items1 in result1.items():
            key2 = cluster_map[key1]
            items2 = result2[key2]
            
            # Check that the same items are in both clusters
            self.assertEqual(
                sorted([item["id"] for item in items1]),
                sorted([item["id"] for item in items2]),
                "Same items should be in the corresponding clusters in both runs"
            )

    def test_large_dataset_performance(self):
        """Test clustering performance on a larger dataset."""
        n_clusters = 3
        modality = "audio"
        
        # Skip if we don't have the large sample data
        if not hasattr(self.__class__, 'large_sample_data') or not self.__class__.large_sample_data:
            self.skipTest("Large sample data not available")
        
        # Measure processing time
        start_time = time.time()
        result = self.operator.run(self.large_sample_data, n_clusters=n_clusters, modality=modality)
        processing_time = time.time() - start_time
        
        # Store benchmark result
        self.__class__.benchmark_results['large_dataset_clustering_time'] = processing_time
        
        # Assert that processing time is reasonable (adjust thresholds as needed)
        self.assertLess(processing_time, 30, "Clustering should take less than 30 seconds")
        print(f"Large dataset clustering time: {processing_time:.2f} seconds")
        
        # Check that all items were assigned to clusters
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        self.assertEqual(len(all_items), len(self.large_sample_data), 
                         "All items should be assigned to a cluster")
        
        # Check that we have the expected number of clusters
        self.assertEqual(len(result), n_clusters, f"Should have {n_clusters} clusters")

    def test_high_dimensional_data(self):
        """Test clustering with high-dimensional data."""
        n_clusters = 3
        modality = "audio"
        
        # Skip if we don't have the high-dimensional data
        if not hasattr(self.__class__, 'high_dim_data') or not self.__class__.high_dim_data:
            self.skipTest("High-dimensional data not available")
        
        result = self.operator.run(self.high_dim_data, n_clusters=n_clusters, modality=modality)
        
        # Check that all items were assigned to clusters
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        self.assertEqual(len(all_items), len(self.high_dim_data), 
                         "All items should be assigned to a cluster")
        
        # Check that we have the expected number of clusters
        self.assertEqual(len(result), n_clusters, f"Should have {n_clusters} clusters")

    def test_edge_case_empty_input(self):
        """Test handling of empty input data."""
        empty_data = []
        
        # This should raise an exception or return an empty result
        with self.assertRaises(Exception) as context:
            self.operator.run(empty_data, n_clusters=3, modality="audio")
        
        # The exact exception depends on the implementation
        print(f"Empty data exception: {context.exception}")

    def test_edge_case_single_item(self):
        """Test clustering with just a single item."""
        single_item_data = [
            {"embedding": [1.0, 2.0, 3.0], "payload": {"id": "item1", "metadata": "data1"}}
        ]
        
        # Set n_clusters=1 since we only have one item
        result = self.operator.run(single_item_data, n_clusters=1, modality="audio")
        
        # Check that the item was assigned to a cluster
        self.assertEqual(len(result), 1, "Should have 1 cluster")
        
        # Check that the item is in the cluster
        cluster_key = list(result.keys())[0]
        self.assertEqual(len(result[cluster_key]), 1, "Cluster should have 1 item")
        self.assertEqual(result[cluster_key][0]["id"], "item1", "Item should be in the cluster")

    def test_stability_with_varying_clusters(self):
        """Test the stability of clustering with different numbers of clusters."""
        modality = "audio"
        stability_results = {}
        
        # Test with different numbers of clusters
        for n_clusters in [2, 3, 4, 5]:
            result = self.operator.run(self.sample_data, n_clusters=n_clusters, modality=modality)
            
            # Track how many clusters were created
            n_actual_clusters = len(result)
            stability_results[n_clusters] = n_actual_clusters
            
            # Verify that all items were assigned to clusters
            all_items = []
            for cluster_items in result.values():
                all_items.extend(cluster_items)
            self.assertEqual(len(all_items), len(self.sample_data), 
                             f"All items should be assigned to a cluster when n_clusters={n_clusters}")
        
        # Print stability results
        print("\n=== Cluster Stability Results ===")
        for requested, actual in stability_results.items():
            print(f"Requested clusters: {requested}, Actual clusters: {actual}")
        
        # Store the stability results for teardown reporting
        self.__class__.benchmark_results['stability_results'] = stability_results

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
                    if key == 'stability_results':
                        # Skip this as it was already printed
                        continue
                    print(f"{key}: {value}")
                print("=====================================")
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")