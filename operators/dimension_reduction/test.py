import numpy as np
import pytest

from operators.dimension_reduction.dimension_reduction import (
    DimensionReduction,
    ReductionModel,
    TSNEReduction,
    UMAPReduction,
)


def generate_input_data(num_samples: int = 100, dimensions: int = 50):
    sample_embeddings = np.random.rand(num_samples, dimensions)
    input_data = [
        {"payload": str(i), "embedding": embedding.tolist()}
        for i, embedding in enumerate(sample_embeddings)
    ]
    return input_data, sample_embeddings


class TestTSNEReduction:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.params = {
            "n_components": 2,
            "perplexity": 30,
            "learning_rate": 200,
            "max_iter": 250,
            "random_state": 42,
        }
        self.input_data, _ = generate_input_data()

    def test_output_shape_and_payload(self):
        operator = DimensionReduction("tsne", self.params)
        reduced = operator.run(self.input_data)

        assert len(reduced) == len(self.input_data)
        assert all("payload" in d and "reduced_embedding" in d for d in reduced)

        emb = np.array([d["reduced_embedding"] for d in reduced])
        assert emb.shape == (len(self.input_data), self.params["n_components"])


class TestUMAPReduction:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.params = {
            "n_components": 2,
            "n_neighbors": 10,
            "min_dist": 0.1,
            "random_state": 42,
        }
        self.input_data, _ = generate_input_data()

    def test_output_shape_and_payload(self):
        operator = DimensionReduction("umap", self.params)
        reduced = operator.run(self.input_data)

        assert len(reduced) == len(self.input_data)
        assert all("payload" in d and "reduced_embedding" in d for d in reduced)

        emb = np.array([d["reduced_embedding"] for d in reduced])
        assert emb.shape == (len(self.input_data), self.params["n_components"])


class TestDimensionReductionValidation:
    def test_invalid_model_type(self):
        with pytest.raises(ValueError, match="Unsupported model type"):
            DimensionReduction("bogus", {})

    def test_empty_input_list(self):
        operator = DimensionReduction("umap", {"n_components": 2})
        with pytest.raises(ValueError, match="non-empty list"):
            operator.run([])

    def test_missing_keys(self):
        operator = DimensionReduction("tsne", {"n_components": 2})
        with pytest.raises(KeyError):
            operator.run([{"embedding": [0.1, 0.2]}])  # Missing payload
        with pytest.raises(KeyError):
            operator.run([{"payload": "x"}])  # Missing embedding

    def test_invalid_embeddings(self):
        operator = DimensionReduction("tsne", {"n_components": 2})

        # Non-numeric embedding
        with pytest.raises(ValueError):
            operator.run([{"payload": "x", "embedding": ["a", "b", "c"]}])

        # Embedding with NaN
        with pytest.raises(ValueError):
            operator.run([{"payload": "x", "embedding": [1.0, float("nan")]}])

        # Embedding with inf
        with pytest.raises(ValueError):
            operator.run([{"payload": "x", "embedding": [1.0, float("inf")]}])

    def test_single_point_error(self):
        operator = DimensionReduction("tsne", {"n_components": 2, "perplexity": 5})
        with pytest.raises(RuntimeError, match="must be less than n_samples"):
            operator.run([{"payload": "x", "embedding": list(np.random.rand(50))}])


class TestFactoryLogic:
    def test_factory_instantiates_models_correctly(self):
        tsne = DimensionReduction.get_reduction_model("tsne", {"n_components": 2})
        umap = DimensionReduction.get_reduction_model("umap", {"n_components": 2})
        assert isinstance(tsne, TSNEReduction)
        assert isinstance(umap, UMAPReduction)
        assert isinstance(tsne, ReductionModel)
        assert isinstance(umap, ReductionModel)
