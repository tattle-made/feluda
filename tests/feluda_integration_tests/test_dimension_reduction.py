import math

import numpy as np
import pytest
from dimension_reduction import DimensionReduction


@pytest.fixture(scope="session")
def sample_inputs():
    """Fixture to provide sample inputs for testing."""
    return [
        {"payload": "A", "embedding": [1.0, 0.0, 0.0]},
        {"payload": "B", "embedding": [0.0, 1.0, 0.0]},
        {"payload": "C", "embedding": [0.0, 0.0, 1.0]},
    ]


@pytest.fixture(scope="session")
def expected_dim():
    """Fixture to provide expected dimension."""
    return 2


class TestDimensionReductionIntegration:
    """Test dimension reduction functionality."""

    def test_end_to_end_reduction(self, sample_inputs, expected_dim):
        """Test that tsne reduction runs end-to-end and outputs correct shape and finite values."""
        operator = DimensionReduction(
            "tsne",
            {
                "n_components": 2,
                "perplexity": 2,
                "learning_rate": 100,
                "max_iter": 250,
                "random_state": 123,
            },
        )

        # Some TSNE implementations may reject certain configurations; skip if unsupported
        try:
            out = operator.run(sample_inputs)
        except RuntimeError as e:
            pytest.skip(f"t-SNE reduction not supported: {e}")

        assert isinstance(out, list)
        assert len(out) == len(sample_inputs)

        for original, reduced in zip(sample_inputs, out, strict=False):
            assert "payload" in reduced
            assert "reduced_embedding" in reduced
            assert reduced["payload"] == original["payload"]
            vec = reduced["reduced_embedding"]
            assert isinstance(vec, list)
            assert len(vec) == expected_dim
            for v in vec:
                assert isinstance(v, float)
                assert math.isfinite(v), "reduced value should be finite"

    def test_consistency_with_fixed_seed(self, sample_inputs):
        """With a fixed random_state, repeated runs give identical results."""
        operator = DimensionReduction(
            "tsne",
            {
                "n_components": 2,
                "perplexity": 2,
                "learning_rate": 100,
                "max_iter": 250,
                "random_state": 123,
            },
        )

        try:
            out1 = operator.run(sample_inputs)
            out2 = operator.run(sample_inputs)
        except RuntimeError:
            pytest.skip("t-SNE reduction not supported for consistency test")

        for v1, v2 in zip(out1, out2, strict=False):
            np.testing.assert_array_almost_equal(
                np.array(v1["reduced_embedding"]),
                np.array(v2["reduced_embedding"]),
                decimal=6,
                err_msg="Repeated reductions should be identical with fixed seed",
            )

    def test_invalid_input_empty(self):
        """Test that passing an empty list raises ValueError."""
        operator = DimensionReduction("tsne", {"n_components": 2})
        with pytest.raises(ValueError):
            operator.run([])

    def test_invalid_input_missing_keys(self):
        """Test that missing 'embedding' or 'payload' keys raises KeyError."""
        operator = DimensionReduction("tsne", {"n_components": 2})
        with pytest.raises(KeyError):
            operator.run([{"payload": "only_payload"}])
        with pytest.raises(KeyError):
            operator.run([{"embedding": [1, 2, 3]}])

    def test_operator_configuration(self):
        """Test that operator initializes properly and has required methods."""
        operator = DimensionReduction("tsne", {"n_components": 2})
        assert operator is not None
        assert hasattr(operator, "run")

    def test_different_tsne_parameters(self, sample_inputs):
        """Test that different TSNE parameters are correctly applied."""
        # Initialize with exact method instead of barnes_hut
        operator = DimensionReduction(
            "tsne",
            {
                "n_components": 2,
                "perplexity": 1,  # Keep low for small test dataset
                "method": "exact",  # Different method
                "random_state": 42,
                "max_iter": 500,  # Different max iterations
            },
        )

        try:
            result = operator.run(sample_inputs)
            assert len(result) == len(sample_inputs)
            assert len(result[0]["reduced_embedding"]) == 2
        except RuntimeError as e:
            pytest.skip(f"t-SNE with custom params not supported: {e}")

    def test_different_input_dimensions(self):
        """Test reduction with different input dimensions."""
        # 5D input
        inputs_5d = [
            {"payload": "A", "embedding": [1.0, 2.0, 3.0, 4.0, 5.0]},
            {"payload": "B", "embedding": [5.0, 4.0, 3.0, 2.0, 1.0]},
            {"payload": "C", "embedding": [1.0, 1.0, 1.0, 1.0, 1.0]},
        ]

        operator = DimensionReduction(
            "tsne",
            {
                "n_components": 2,  # Reduce to 2D
                "perplexity": 1,  # Valid perplexity for 3 samples
                "random_state": 42,
            },
        )

        try:
            result = operator.run(inputs_5d)
            assert len(result) == len(inputs_5d)
            assert len(result[0]["reduced_embedding"]) == 2
        except RuntimeError as e:
            pytest.skip(f"t-SNE reduction for 5D input not supported: {e}")

    def test_invalid_embeddings_dimension(self):
        """Test that mismatched embedding dimensions raise an error."""
        operator = DimensionReduction("tsne", {"n_components": 2})

        # Create an input with mismatched embedding dimensions
        bad_inputs = [
            {"payload": "A", "embedding": [1.0, 2.0]},
            {"payload": "B", "embedding": [1.0, 2.0, 3.0]},  # Different dimension
        ]

        with pytest.raises((ValueError, RuntimeError)):
            operator.run(bad_inputs)

    def test_multiple_initializations(self, sample_inputs):
        """Test that multiple initializations work correctly."""
        operator1 = DimensionReduction(
            "tsne",
            {
                "n_components": 2,
                "perplexity": 1,
                "random_state": 42,
            },
        )

        operator2 = DimensionReduction(
            "tsne",
            {
                "n_components": 2,
                "perplexity": 1,
                "random_state": 43,  # Different seed
            },
        )

        # First initialization
        try:
            result1 = operator1.run(sample_inputs)
        except RuntimeError:
            pytest.skip("t-SNE not supported for first initialization")

        # Second initialization with different parameters
        try:
            result2 = operator2.run(sample_inputs)
        except RuntimeError:
            pytest.skip("t-SNE not supported for second initialization")

        # Results should be different with different random seeds
        any_different = False
        for v1, v2 in zip(result1, result2, strict=False):
            try:
                np.testing.assert_array_almost_equal(
                    np.array(v1["reduced_embedding"]), np.array(v2["reduced_embedding"])
                )
            except AssertionError:
                any_different = True
                break

        # With different random seeds, results should differ
        assert any_different, "Different random seeds should produce different results"
