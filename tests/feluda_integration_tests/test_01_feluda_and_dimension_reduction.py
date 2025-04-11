import tempfile
import unittest
from pathlib import Path

import numpy as np
import yaml

from feluda import Feluda


class TestFeludaDimensionReductionIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Base configuration for tests."""
        cls.base_config = {
            "operators": {
                "label": "Operators",
                "parameters": []  # Will be set up per test case
            }
        }

    def _setup_feluda_with_ncomponents(self, n_components, num_samples=None):
        """Helper to initialize Feluda with given n_components and auto-compute perplexity.

        If num_samples is provided, perplexity is set to min(30, num_samples-1). Otherwise, a default value of 30 is used.
        """
        perplexity = min(30, num_samples - 1) if num_samples and num_samples > 0 else 30  #To set perplexity default as 30.

        model_params = {
            "model_type": "tsne",
            "n_components": n_components,
            "perplexity": perplexity,
            "learning_rate": 200,
            "n_iter": 500,
            "random_state": 42,
        }
        config = self.base_config.copy()
        config["operators"]["parameters"] = [{
            "name": "dimension reduction",
            "type": "dimension_reduction",
            "parameters": model_params,
        }]

        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        yaml.dump(config, temp_file)
        temp_file.close()
        self._temp_config_path = temp_file.name

        feluda = Feluda(self._temp_config_path)
        feluda.setup()
        return feluda

    def test_dimensionality_reduction(self):
        """Test that 2D dimensionality reduction works end-to-end with proper perplexity."""
        num_samples = 100
        embedding_dim = 20
        sample_embeddings = np.random.rand(num_samples, embedding_dim)  # 100 samples, 20 dimensions

        input_data = [{"payload": str(i), "embedding": embedding.tolist()} for i, embedding in enumerate(sample_embeddings)]
        feluda = self._setup_feluda_with_ncomponents(n_components=2, num_samples=num_samples) #Reduction to 2D
        operator = feluda.operators.get()["dimension_reduction"]
        reduced_data = operator.run(input_data)

        self.assertEqual(len(reduced_data), num_samples)
        for item in reduced_data:
            self.assertIn("payload", item)
            self.assertIn("reduced_embedding", item)
            self.assertEqual(len(item["reduced_embedding"]), 2)

    def test_3d_dimensionality_reduction(self):
        """Test that dimensionality reduction works for 3D output."""
        num_samples = 50
        embedding_dim = 20
        sample_embeddings = np.random.rand(num_samples, embedding_dim)

        input_data = [{"payload": str(i), "embedding": embedding.tolist()} for i, embedding in enumerate(sample_embeddings)]

        feluda = self._setup_feluda_with_ncomponents(n_components=3, num_samples=num_samples) #Reduction to 3D
        operator = feluda.operators.get()["dimension_reduction"]
        reduced_data = operator.run(input_data)

        self.assertEqual(len(reduced_data), num_samples)
        for item in reduced_data:
            self.assertIn("payload", item)
            self.assertIn("reduced_embedding", item)
            self.assertEqual(len(item["reduced_embedding"]), 3)

    def test_invalid_input(self):
        """Test handling of invalid inputs."""
        # For invalid input tests, we can use an arbitrary num_samples to set perplexity
        feluda = self._setup_feluda_with_ncomponents(n_components=2, num_samples=10) #Reduction to 2D
        operator = feluda.operators.get()["dimension_reduction"]

        with self.assertRaises(ValueError):
            operator.run([])  # Empty list test

        with self.assertRaises(KeyError):
            operator.run([{"payload": "123"}])  # Missing embedding

    def test_high_dimensional_input(self):
        """Ensure the model works with high-dimensional embeddings."""
        num_samples = 20
        embedding_dim = 100
        sample_embeddings = np.random.rand(num_samples, embedding_dim)

        input_data = [{"payload": str(i), "embedding": embedding.tolist()} for i, embedding in enumerate(sample_embeddings)]

        feluda = self._setup_feluda_with_ncomponents(n_components=2, num_samples=num_samples)
        operator = feluda.operators.get()["dimension_reduction"]
        reduced_data = operator.run(input_data)

        self.assertEqual(len(reduced_data), num_samples)
        for item in reduced_data:
            self.assertEqual(len(item["reduced_embedding"]), 2) #Reduction to 2D

    def test_operator_configuration(self):
        """Test that operator is properly configured."""
        feluda = self._setup_feluda_with_ncomponents(n_components=2, num_samples=10) #Reduction to 2D
        operator = feluda.operators.get()["dimension_reduction"]
        self.assertIsNotNone(operator, "Operator should be properly initialized")
        self.assertTrue(hasattr(operator, "run"), "Operator should have 'run' method")

    def tearDown(self):
        """Remove the temporary config file after each test."""
        if hasattr(self, '_temp_config_path'):
            Path(self._temp_config_path).unlink()

if __name__ == "__main__":
    unittest.main()
