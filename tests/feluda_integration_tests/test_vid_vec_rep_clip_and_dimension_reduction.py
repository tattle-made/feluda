import numpy as np
import pytest
from dimension_reduction import DimensionReduction
from vid_vec_rep_clip import VidVecRepClip

from feluda.factory import VideoFactory


@pytest.fixture(scope="session")
def video_operator():
    """Fixture to provide video vector representation operator."""
    return VidVecRepClip()


@pytest.fixture(scope="session")
def test_video_url():
    """Fixture to provide test video URL."""
    return "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"


@pytest.fixture(scope="session")
def video_vectors(video_operator, test_video_url):
    """Fixture to provide video vectors for testing."""
    vecs = list(video_operator.run(VideoFactory.make_from_url(test_video_url)))
    if len(vecs) < 3:
        raise RuntimeError(f"Need ≥3 embeddings but got {len(vecs)}")

    return {
        "avg_vec": vecs[0]["vid_vec"],
        "frame_vecs": [vecs[1]["vid_vec"], vecs[2]["vid_vec"]],
        "expected_dim": len(vecs[0]["vid_vec"]),
    }


@pytest.fixture(scope="session")
def video_vectors_for_umap(video_operator, test_video_url):
    """Fixture to provide video vectors for UMAP testing."""
    vecs = list(video_operator.run(VideoFactory.make_from_url(test_video_url)))
    needed = 5
    if len(vecs) < needed:
        raise RuntimeError(f"Need ≥{needed} embeddings but got {len(vecs)}")

    return [v["vid_vec"] for v in vecs[:needed]]


class TestTSNEIntegration:
    """Test t-SNE dimension reduction integration."""

    def test_smoke_video_and_tsne(self, video_vectors):
        """Smoke: two 512d → TSNE→ two 2d embeddings."""
        dr_operator = DimensionReduction(
            "tsne", {"n_components": 2, "perplexity": 1, "random_state": 42}
        )

        data = [
            {"payload": "avg", "embedding": video_vectors["avg_vec"]},
            {"payload": "f1", "embedding": video_vectors["frame_vecs"][0]},
        ]

        out = dr_operator.run(data)
        assert len(out) == 2
        for item in out:
            assert "reduced_embedding" in item
            assert len(item["reduced_embedding"]) == 2

    def test_tsne_seed_consistency(self, video_vectors):
        """Fixed-seed TSNE on the same two vectors yields identical outputs."""
        dr_operator = DimensionReduction(
            "tsne", {"n_components": 2, "perplexity": 1, "random_state": 42}
        )

        data = [
            {"payload": "avg", "embedding": video_vectors["avg_vec"]},
            {"payload": "f1", "embedding": video_vectors["frame_vecs"][0]},
        ]

        a = dr_operator.run(data)
        b = dr_operator.run(data)

        for x, y in zip(a, b, strict=False):
            np.testing.assert_allclose(x["reduced_embedding"], y["reduced_embedding"])

    def test_full_video_to_tsne_pipeline(self, video_vectors):
        """End-to-end video→TSNE preserves payloads and dims."""
        dr_operator = DimensionReduction(
            "tsne", {"n_components": 2, "perplexity": 1, "random_state": 42}
        )

        data = [
            {"payload": "avg", "embedding": video_vectors["avg_vec"]},
            {"payload": "f2", "embedding": video_vectors["frame_vecs"][1]},
        ]

        out = dr_operator.run(data)
        got = [o["payload"] for o in out]
        assert sorted(got) == sorted(["avg", "f2"])

        for o in out:
            assert len(o["reduced_embedding"]) == 2


class TestUMAPIntegration:
    """Test UMAP dimension reduction integration."""

    def test_umap_integration(self, video_vectors_for_umap):
        """UMAP: avg + frames → 3d embeddings."""
        dr_operator = DimensionReduction(
            "umap", {"n_components": 3, "n_neighbors": 2, "random_state": 42}
        )

        data = [
            {"payload": f"p{i}", "embedding": vec}
            for i, vec in enumerate(video_vectors_for_umap)
        ]

        out = dr_operator.run(data)
        assert len(out) == len(video_vectors_for_umap)

        for item in out:
            assert len(item["reduced_embedding"]) == 3


class TestDimensionReductionValidation:
    """Test dimension reduction validation and error handling."""

    def test_invalid_model_type(self):
        """Test that invalid model type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported model type"):
            DimensionReduction("bogus", {})

    def test_empty_input_list(self):
        """Test that empty input list raises ValueError."""
        operator = DimensionReduction("umap", {"n_components": 2})
        with pytest.raises(ValueError, match="non-empty list"):
            operator.run([])

    def test_missing_keys(self):
        """Test that missing required keys raises KeyError."""
        operator = DimensionReduction("tsne", {"n_components": 2})

        with pytest.raises(KeyError):
            operator.run([{"embedding": [0.1, 0.2]}])  # Missing payload

        with pytest.raises(KeyError):
            operator.run([{"payload": "x"}])  # Missing embedding

    def test_invalid_embeddings(self):
        """Test that invalid embeddings raise appropriate errors."""
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
        """Test that single point with high perplexity raises error."""
        operator = DimensionReduction("tsne", {"n_components": 2, "perplexity": 5})
        with pytest.raises(RuntimeError, match="must be less than n_samples"):
            operator.run([{"payload": "x", "embedding": list(np.random.rand(50))}])


@pytest.fixture(scope="session", autouse=True)
def cleanup_operators(video_operator):
    """Cleanup operators after each test."""
    yield
    video_operator.cleanup()
