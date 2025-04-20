import unittest

import numpy as np

from operators.dimension_reduction.dimension_reduction import (
    DimensionReductionFactory,
    initialize,
    run,
)


# Helper data generation
def generate_input_data(num_samples=100, dimensions=50):
    """Generates sample input data for testing."""
    sample_embeddings = np.random.rand(num_samples, dimensions)
    input_data = [
        {"payload": str(i), "embedding": embedding.tolist()}
        for i, embedding in enumerate(sample_embeddings)
    ]
    return input_data, sample_embeddings


class TestTSNEReductionOperator(unittest.TestCase):
    """Tests specifically for the t-SNE reduction."""

    @classmethod
    def setUpClass(cls):
        """Initialize the t-SNE model once for all tests in this class."""
        print("\nSetting up t-SNE tests...")
        cls.tsne_params = {
            "model_type": "tsne",
            "n_components": 2,
            "perplexity": 30,
            "learning_rate": 200,
            "max_iter": 250,
            "random_state": 42,
            "method": "barnes_hut",
        }
        initialize(cls.tsne_params)
        print("t-SNE model initialized for tests.")

        cls.input_data, cls.original_embeddings = generate_input_data(num_samples=100)

    @classmethod
    def tearDownClass(cls):
        """Clean up after t-SNE tests if necessary."""
        pass

    def test_tsne_reduction_output_shape(self):
        """Verify t-SNE reduces to the correct shape."""
        reduced_data = run(self.input_data)
        self.assertEqual(
            len(reduced_data),
            len(self.input_data),
            "Number of items should match input",
        )
        reduced_embeddings = np.array([d["reduced_embedding"] for d in reduced_data])
        self.assertEqual(
            reduced_embeddings.shape,
            (len(self.input_data), self.tsne_params["n_components"]),
        )

    def test_tsne_reduction_payload_preservation(self):
        """Verify payloads are correctly preserved."""
        reduced_data = run(self.input_data)
        original_payloads = [d["payload"] for d in self.input_data]
        reduced_payloads = [d["payload"] for d in reduced_data]
        self.assertEqual(original_payloads, reduced_payloads)


class TestUMAPReductionOperator(unittest.TestCase):
    """Tests specifically for the UMAP reduction."""

    @classmethod
    def setUpClass(cls):
        """Initialize the UMAP model once for all tests in this class."""
        print("\nSetting up UMAP tests...")
        cls.umap_params = {
            "model_type": "umap",
            "n_components": 2,
            "n_neighbors": 5,
            "min_dist": 0.1,
            "random_state": 42,
        }
        initialize(cls.umap_params)
        print("UMAP model initialized for tests.")

        cls.input_data, cls.original_embeddings = generate_input_data(num_samples=100)

    @classmethod
    def tearDownClass(cls):
        """Clean up after UMAP tests if necessary."""
        pass

    def test_umap_reduction_output_shape(self):
        """Verify UMAP reduces to the correct shape."""
        reduced_data = run(self.input_data)
        self.assertEqual(
            len(reduced_data),
            len(self.input_data),
            "Number of items should match input",
        )
        reduced_embeddings = np.array([d["reduced_embedding"] for d in reduced_data])
        self.assertEqual(
            reduced_embeddings.shape,
            (len(self.input_data), self.umap_params["n_components"]),
        )

    def test_umap_reduction_payload_preservation(self):
        """Verify payloads are correctly preserved."""
        reduced_data = run(self.input_data)
        original_payloads = [d["payload"] for d in self.input_data]
        reduced_payloads = [d["payload"] for d in reduced_data]
        self.assertEqual(original_payloads, reduced_payloads)


class TestDimensionReductionGeneral(unittest.TestCase):
    """Tests for general functionality and error handling."""

    def test_invalid_input_run(self):
        """Test run function with various invalid inputs."""
        initialize({})

        # Test with empty list
        with self.assertRaisesRegex(ValueError, "Input should be a non-empty list"):
            run([])

        # Test with non-list input
        with self.assertRaisesRegex(ValueError, "Input should be a non-empty list"):
            run("not a list")

        # Test with missing 'embedding' key
        with self.assertRaisesRegex(KeyError, "Missing key: 'embedding'"):
            run([{"payload": "123"}])

        # Test with missing 'payload' key
        with self.assertRaisesRegex(KeyError, "Missing key: 'payload'"):
            run([{"embedding": [1, 2, 3]}])

    def test_invalid_model_type_initialize(self):
        """Test initialize function with an unsupported model type."""
        with self.assertRaisesRegex(
            ValueError, "Unsupported model type: invalid_model"
        ):
            initialize({"model_type": "invalid_model"})

    def test_factory_invalid_type(self):
        """Test the factory directly with an invalid type."""
        with self.assertRaisesRegex(
            ValueError, "Unsupported model type: non_existent_model"
        ):
            DimensionReductionFactory.get_reduction_model("non_existent_model")
