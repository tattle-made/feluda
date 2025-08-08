import pytest
from cluster_embeddings import ClusterEmbeddings

from feluda.factory import AudioFactory


@pytest.fixture(scope="session")
def cluster_operator():
    """Fixture to provide cluster embeddings operator."""
    return ClusterEmbeddings()


@pytest.fixture(scope="session")
def test_audio_url():
    """Fixture to provide test audio URL."""
    return "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/audio.wav"


class TestClusterEmbeddingsIntegration:
    """Test cluster embeddings functionality."""

    @pytest.skip("audio file is not available")
    def test_cluster_embeddings(self, cluster_operator, test_audio_url):
        """Test the cluster_embeddings operator."""
        audio_obj = AudioFactory.make_from_url(test_audio_url)
        assert audio_obj is not None, "Audio object should be successfully created"

        print(f"Audio object: {audio_obj}")

        # Generate mock embeddings and payloads for testing
        embedding_1 = [0.1, 0.2, 0.3]  # Mock embedding for sample 1
        embedding_2 = [0.4, 0.5, 0.6]  # Mock embedding for sample 2
        payload_1 = {"path": audio_obj["path"]}
        payload_2 = {"path": audio_obj["path"]}

        # Prepare input_data with at least 2 samples
        input_data = [
            {"embedding": embedding_1, "payload": payload_1},
            {"embedding": embedding_2, "payload": payload_2},
        ]

        result = cluster_operator.run(
            input_data=input_data, n_clusters=2, modality="audio"
        )

        assert "cluster_0" in result
        assert "cluster_1" in result
        assert len(result) == 2


@pytest.fixture(scope="session", autouse=True)
def cleanup_operators(cluster_operator):
    """Cleanup operators after each test."""
    yield
    cluster_operator.cleanup()
