import unittest

from operators.cluster_embeddings import cluster_embeddings

# Test constants
MOCK_DATA = [
    {"payload": "A", "embedding": [0, 1]},
    {"payload": "B", "embedding": [1, 0]},
    {"payload": "C", "embedding": [100, 101]},
    {"payload": "D", "embedding": [101, 100]},
]
EXPECTED_CLUSTERS = [["A", "B"], ["C", "D"]]


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        cluster_embeddings.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_kmeans_clustering(self):
        result = cluster_embeddings.run(
            input_data=MOCK_DATA, n_clusters=2, modality="audio"
        )
        self.assertIn("cluster_0", result)
        self.assertIn("cluster_1", result)
        self.assertEqual(len(result), 2)
        self.assertCountEqual(
            [result["cluster_0"], result["cluster_1"]], EXPECTED_CLUSTERS
        )

    def test_agglomerative_clustering(self):
        result = cluster_embeddings.run(
            input_data=MOCK_DATA, n_clusters=2, modality="video"
        )
        self.assertIn("cluster_0", result)
        self.assertIn("cluster_1", result)
        self.assertEqual(len(result), 2)
        self.assertCountEqual(
            [result["cluster_0"], result["cluster_1"]], EXPECTED_CLUSTERS
        )

    def test_affinity_propagation(self):
        result = cluster_embeddings.run(
            input_data=MOCK_DATA, n_clusters=None, modality="audio"
        )
        self.assertIn("cluster_0", result)
        self.assertIn("cluster_1", result)
        self.assertEqual(len(result), 2)
        self.assertCountEqual(
            [result["cluster_0"], result["cluster_1"]], EXPECTED_CLUSTERS
        )
