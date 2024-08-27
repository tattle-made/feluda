import unittest
import numpy as np
from core.operators.dimension_reduction import setup_reduction, perform_reduction


class TestDimensionReductionOperator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize operator
        cls.initial_params = {
            'n_components': 2,
            'perplexity': 30,
            'learning_rate': 200,
            'max_iter': 250,
            'random_state': 42,
            'method': 'barnes_hut'
        }
        setup_reduction('tsne', cls.initial_params)

    @classmethod
    def tearDownClass(cls):
        # Clean up if necessary
        pass

    def test_tsne_reduction(self):
        # Create sample embeddings
        sample_embeddings = np.random.rand(100, 50)  # 100 samples, 50 dimensions

        input_data = [{'payload': str(i), 'embedding': embedding} for i, embedding in enumerate(sample_embeddings)]

        # Perform reduction
        reduced_data = perform_reduction(input_data)
        reduced_embeddings = np.array([d['reduced_embedding'] for d in reduced_data])

        # Check output shape
        self.assertEqual(reduced_embeddings.shape, (100, 2))  # Should reduce to 2D

    def test_invalid_input(self):
        # Test with empty list
        with self.assertRaises(ValueError):
            perform_reduction([])

        # Test with non-list input
        with self.assertRaises(ValueError):
            perform_reduction("not a list")

        # Test with missing keys in input data
        with self.assertRaises(KeyError):
            perform_reduction([{'payload': '123'}])