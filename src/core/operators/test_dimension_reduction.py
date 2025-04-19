import os
import sys
import unittest

import numpy as np
from dimension_reduction import initialize, run


class TestDimensionReductionOperator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize t-SNE operator
        cls.tsne_params = {
            'model_type': 'tsne',
            'n_components': 2,
            'perplexity': 30,
            'learning_rate': 200,
            'max_iter': 250,
            'random_state': 42,
            'method': 'barnes_hut'
        }
        initialize(cls.tsne_params)

        # Initialize UMAP operator
        umap_params = {
            'model_type': 'umap',
            'n_components': 2,
            'n_neighbors': 15,
            'min_dist': 0.1,
            'random_state': 42,
        }
        initialize(umap_params)
    @classmethod
    def tearDownClass(cls):
        # Clean up if necessary
        pass

    def test_tsne_reduction(self):
        # Create sample embeddings
        sample_embeddings = np.random.rand(100, 50)  # 100 samples, 50 dimensions

        input_data = [{'payload': str(i), 'embedding': embedding} for i, embedding in enumerate(sample_embeddings)]

        # Perform reduction
        reduced_data = run(input_data)
        reduced_embeddings = np.array([d['reduced_embedding'] for d in reduced_data])

        # Check output shape
        self.assertEqual(reduced_embeddings.shape, (100, 2))  # Should reduce to 2D

    def test_umap_reduction(self):
        # Create sample embeddings
        sample_embeddings = np.random.rand(100, 50)  # 100 samples, 50 dimensions

        input_data = [{'payload': str(i), 'embedding': embedding} for i, embedding in enumerate(sample_embeddings)]

        # Perform reduction
        reduced_data = run(input_data)
        reduced_embeddings = np.array([d['reduced_embedding'] for d in reduced_data])

        # Check output shape
        self.assertEqual(reduced_embeddings.shape, (100, 2))  # Should reduce to 2D

    def test_invalid_input(self):
        # Test with empty list
        with self.assertRaises(ValueError):
            run([])

        # Test with non-list input
        with self.assertRaises(ValueError):
            run("not a list")

        # Test with missing keys in input data
        with self.assertRaises(KeyError):
            run([{'payload': '123'}])

    def test_invalid_model_type(self):
        # Test with an unsupported model type
        with self.assertRaises(ValueError):
            initialize({"model_type": "invalid_model"})
