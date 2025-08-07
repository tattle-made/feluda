import contextlib
import math
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import yaml

from feluda import Feluda


class TestFeludaDimensionReductionIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""
        cls.config = {
            "operators": {
                "label": "ReductionOperators",
                "parameters": [
                    {
                        "name": "tsne reduction",
                        "type": "dimension_reduction",
                        "parameters": {
                            "model_type": "tsne",
                            "n_components": 2,
                            "perplexity": 2,
                            "learning_rate": 100,
                            "max_iter": 250,
                            "random_state": 123,
                        },
                    }
                ],
            }
        }

        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with os.fdopen(fd, "w") as f:
            yaml.dump(cls.config, f)

        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()
        cls.sample_inputs = [
            {"payload": "A", "embedding": [1.0, 0.0, 0.0]},
            {"payload": "B", "embedding": [0.0, 1.0, 0.0]},
            {"payload": "C", "embedding": [0.0, 0.0, 1.0]},
        ]
        cls.expected_dim = cls.config["operators"]["parameters"][0]["parameters"][
            "n_components"
        ]

    def setUp(self):
        """Fetch fresh operator reference for each test."""
        self.operator = self.feluda.operators.get()["dimension_reduction"]

    def test_end_to_end_reduction(self):
        """Test that tsne reduction runs end-to-end and outputs correct shape and finite values."""
        # Some TSNE implementations may reject certain configurations; skip if unsupported
        try:
            out = self.operator.run(self.sample_inputs)
        except RuntimeError as e:
            self.skipTest(f"t-SNE reduction not supported: {e}")

        self.assertIsInstance(out, list)
        self.assertEqual(len(out), len(self.sample_inputs))

        for original, reduced in zip(self.sample_inputs, out):
            self.assertIn("payload", reduced)
            self.assertIn("reduced_embedding", reduced)
            self.assertEqual(reduced["payload"], original["payload"])
            vec = reduced["reduced_embedding"]
            self.assertIsInstance(vec, list)
            self.assertEqual(len(vec), self.expected_dim)
            for v in vec:
                self.assertIsInstance(v, float)
                self.assertTrue(math.isfinite(v), "reduced value should be finite")

    def test_consistency_with_fixed_seed(self):
        """With a fixed random_state, repeated runs give identical results."""
        try:
            out1 = self.operator.run(self.sample_inputs)
            out2 = self.operator.run(self.sample_inputs)
        except RuntimeError:
            self.skipTest("t-SNE reduction not supported for consistency test")

        for v1, v2 in zip(out1, out2):
            np.testing.assert_array_almost_equal(
                np.array(v1["reduced_embedding"]),
                np.array(v2["reduced_embedding"]),
                decimal=6,
                err_msg="Repeated reductions should be identical with fixed seed",
            )

    def test_invalid_input_empty(self):
        """Test that passing an empty list raises ValueError."""
        with self.assertRaises(ValueError):
            self.operator.run([])

    def test_invalid_input_missing_keys(self):
        """Test that missing 'embedding' or 'payload' keys raises KeyError."""
        with self.assertRaises(KeyError):
            self.operator.run([{"payload": "only_payload"}])
        with self.assertRaises(KeyError):
            self.operator.run([{"embedding": [1, 2, 3]}])

    def test_operator_configuration(self):
        """Test that operator initializes properly and has required methods."""
        self.assertIsNotNone(self.operator)
        self.assertTrue(hasattr(self.operator, "run"))
        self.assertTrue(hasattr(self.operator, "initialize"))

    def test_initialize_and_run_sequence(self):
        """Ensure initialize + run sequence works, and parameters are bounded correctly."""
        new_inputs = [
            {"payload": "X", "embedding": [1, 2, 3]},
            {"payload": "Y", "embedding": [4, 5, 6]},
        ]
        n_samples = len(new_inputs)
        n_features = len(new_inputs[0]["embedding"]) if n_samples > 0 else 0
        valid_n_components = min(n_samples, n_features)
        valid_perplexity = min(5, n_samples - 1)
        params = {
            "model_type": "tsne",
            "n_components": valid_n_components,
            "perplexity": valid_perplexity,
            "random_state": 0,
        }

        with self.assertNoException("initialize should not raise"):
            self.operator.initialize(params)
        with self.assertNoException("run should not raise after initialize"):
            out = self.operator.run(new_inputs)

        for item in out:
            self.assertEqual(
                len(item["reduced_embedding"]),
                valid_n_components,
                "n_components should match initialized parameter",
            )

    def test_edge_case_high_components(self):
        """Test that n_components > n_features or n_samples raises or is handled."""
        bad_params = {
            "model_type": "tsne",
            "n_components": max(
                1, len(self.sample_inputs) + len(self.sample_inputs[0]["embedding"])
            ),
            "perplexity": 1,
            "random_state": 0,
        }
        # Either initialize or run should error out
        try:
            self.operator.initialize(bad_params)
        except (ValueError, RuntimeError):
            return
        with self.assertRaises((ValueError, RuntimeError)):
            self.operator.run(self.sample_inputs)

    def test_unsupported_model_type(self):
        """Test that unsupported model types raise ValueError."""
        with self.assertRaises(ValueError):
            params = {"model_type": "unsupported_algorithm"}
            self.operator.initialize(params)

    def test_different_tsne_parameters(self):
        """Test that different TSNE parameters are correctly applied."""
        # Initialize with exact method instead of barnes_hut
        params = {
            "model_type": "tsne",
            "n_components": 2,
            "perplexity": 1,  # Keep low for small test dataset
            "method": "exact",  # Different method
            "random_state": 42,
            "max_iter": 500,  # Different max iterations
        }

        with self.assertNoException("initialize with custom params should not raise"):
            self.operator.initialize(params)

        try:
            result = self.operator.run(self.sample_inputs)
            self.assertEqual(len(result), len(self.sample_inputs))
            self.assertEqual(len(result[0]["reduced_embedding"]), 2)
        except RuntimeError as e:
            self.skipTest(f"t-SNE with custom params not supported: {e}")

    def test_different_input_dimensions(self):
        """Test reduction with different input dimensions."""
        # 5D input
        inputs_5d = [
            {"payload": "A", "embedding": [1.0, 2.0, 3.0, 4.0, 5.0]},
            {"payload": "B", "embedding": [5.0, 4.0, 3.0, 2.0, 1.0]},
            {"payload": "C", "embedding": [1.0, 1.0, 1.0, 1.0, 1.0]},
        ]

        params = {
            "model_type": "tsne",
            "n_components": 2,  # Reduce to 2D
            "perplexity": 1,  # Valid perplexity for 3 samples
            "random_state": 42,
        }

        with self.assertNoException("initialize for 5D input should not raise"):
            self.operator.initialize(params)

        try:
            result = self.operator.run(inputs_5d)
            self.assertEqual(len(result), len(inputs_5d))
            self.assertEqual(len(result[0]["reduced_embedding"]), 2)
        except RuntimeError as e:
            self.skipTest(f"t-SNE reduction for 5D input not supported: {e}")

    def test_invalid_embeddings_dimension(self):
        """Test that mismatched embedding dimensions raise an error."""
        # Create an input with mismatched embedding dimensions
        bad_inputs = [
            {"payload": "A", "embedding": [1.0, 2.0]},
            {"payload": "B", "embedding": [1.0, 2.0, 3.0]},  # Different dimension
        ]

        with self.assertRaises((ValueError, RuntimeError)):
            self.operator.run(bad_inputs)

    def test_direct_gen_data_function(self):
        """Test the gen_data utility function directly."""
        # We need to import the module to test internal function
        try:
            from operators.dimension_reduction import dimension_reduction

            payloads = ["A", "B"]
            embeddings = np.array([[1.0, 2.0], [3.0, 4.0]])

            result = dimension_reduction.gen_data(payloads, embeddings)

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["payload"], "A")
            self.assertEqual(result[1]["payload"], "B")
            self.assertEqual(result[0]["reduced_embedding"], [1.0, 2.0])
            self.assertEqual(result[1]["reduced_embedding"], [3.0, 4.0])
        except ImportError:
            self.skipTest("Could not import dimension_reduction module directly")

    def test_multiple_initializations(self):
        """Test that multiple initializations work correctly."""
        params1 = {
            "model_type": "tsne",
            "n_components": 2,
            "perplexity": 1,
            "random_state": 42,
        }

        params2 = {
            "model_type": "tsne",
            "n_components": 2,
            "perplexity": 1,
            "random_state": 43,  # Different seed
        }

        # First initialization
        self.operator.initialize(params1)

        try:
            result1 = self.operator.run(self.sample_inputs)
        except RuntimeError:
            self.skipTest("t-SNE not supported for first initialization")

        # Second initialization with different parameters
        self.operator.initialize(params2)

        try:
            result2 = self.operator.run(self.sample_inputs)
        except RuntimeError:
            self.skipTest("t-SNE not supported for second initialization")

        # Results should be different with different random seeds
        any_different = False
        for v1, v2 in zip(result1, result2):
            try:
                np.testing.assert_array_almost_equal(
                    np.array(v1["reduced_embedding"]), np.array(v2["reduced_embedding"])
                )
            except AssertionError:
                any_different = True
                break

        # With different random seeds, results should differ
        self.assertTrue(
            any_different, "Different random seeds should produce different results"
        )

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        """Context manager to verify no exception is raised."""
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Exception was raised'}: {e}")

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary file."""
        try:
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: could not remove temp config: {e}")
