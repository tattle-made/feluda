import numpy as np
import pytest
from cluster_embeddings import ClusterEmbeddings
from vid_vec_rep_clip import VidVecRepClip

from feluda.factory import VideoFactory


@pytest.fixture(scope="session")
def video_operator():
    """Fixture to provide video vector representation operator."""
    return VidVecRepClip()


@pytest.fixture(scope="session")
def cluster_operator():
    """Fixture to provide cluster embeddings operator."""
    return ClusterEmbeddings()


@pytest.fixture(scope="module")
def test_video_url():
    """Fixture to provide test video URL."""
    return "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"


@pytest.fixture(scope="module")
def expected_vector_dim():
    """Fixture to provide expected vector dimension."""
    return 512


@pytest.fixture(scope="module")
def sample_clustering_data():
    """Fixture to provide sample data for clustering tests."""
    return [
        {
            "embedding": [1.0, 2.0, 3.0],
            "payload": {"id": "item1", "metadata": "data1"},
        },
        {
            "embedding": [1.1, 2.1, 3.1],
            "payload": {"id": "item2", "metadata": "data2"},
        },
        {
            "embedding": [10.0, 11.0, 12.0],
            "payload": {"id": "item3", "metadata": "data3"},
        },
        {
            "embedding": [10.2, 11.2, 12.2],
            "payload": {"id": "item4", "metadata": "data4"},
        },
        {
            "embedding": [20.0, 21.0, 22.0],
            "payload": {"id": "item5", "metadata": "data5"},
        },
    ]


class TestVideoVectorGeneration:
    """Test video vector generation functionality."""

    def test_video_vector_generation(
        self, video_operator, test_video_url, expected_vector_dim
    ):
        """Test that video vector generation works end-to-end."""
        video_obj = VideoFactory.make_from_url(test_video_url)
        assert video_obj is not None, "Video object should be successfully created"

        video_vec_generator = video_operator.run(video_obj)

        # Test first vector (average vector)
        first_vec = next(video_vec_generator)
        assert isinstance(first_vec, dict), "Result should be a dictionary"
        assert "vid_vec" in first_vec, "Result should contain 'vid_vec' key"
        assert "is_avg" in first_vec, "Result should contain 'is_avg' key"
        assert first_vec["is_avg"], "First vector should be the average vector"

        # Verify vector dimensions
        vid_vec = first_vec["vid_vec"]
        assert isinstance(vid_vec, list), "Vector should be a list"
        assert len(vid_vec) == expected_vector_dim, (
            f"Vector should have dimension {expected_vector_dim}"
        )

        # Check for I-frame vectors
        i_frame_vectors = []
        for vec_data in video_vec_generator:
            assert not vec_data["is_avg"], (
                "Subsequent vectors should be I-frame vectors"
            )
            i_frame_vectors.append(vec_data["vid_vec"])

        # There should be at least one I-frame
        assert len(i_frame_vectors) > 0, "Should have at least one I-frame vector"

        # All vectors should have the same dimension
        for vec in i_frame_vectors:
            assert len(vec) == expected_vector_dim, (
                f"All I-frame vectors should have dimension {expected_vector_dim}"
            )

    def test_video_vector_consistency(self, video_operator, test_video_url):
        """Test that generating vectors twice from the same video gives consistent results."""
        # First vector generation
        video_obj = VideoFactory.make_from_url(test_video_url)
        vec1_generator = video_operator.run(video_obj)
        vec1 = next(vec1_generator)["vid_vec"]

        # Second vector generation with a new video object
        video_obj = VideoFactory.make_from_url(test_video_url)
        vec2_generator = video_operator.run(video_obj)
        vec2 = next(vec2_generator)["vid_vec"]

        # Vectors should be nearly identical (floating point comparison)
        np.testing.assert_almost_equal(
            vec1,
            vec2,
            decimal=5,
            err_msg="Vectors should be nearly identical for the same video",
        )


class TestClusterEmbeddings:
    """Test cluster embeddings functionality."""

    def test_kmeans_clustering(self, cluster_operator, sample_clustering_data):
        """Test KMeans clustering with audio modality."""
        n_clusters = 3
        modality = "audio"

        result = cluster_operator.run(
            sample_clustering_data, n_clusters=n_clusters, modality=modality
        )

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert len(result) == n_clusters, f"Should have {n_clusters} clusters"

        # Check that each cluster key follows the expected format
        for key in result:
            assert key.startswith("cluster_"), (
                "Cluster keys should start with 'cluster_'"
            )
            assert isinstance(result[key], list), "Cluster values should be lists"

        # Check that all items are assigned to some cluster
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        assert len(all_items) == len(sample_clustering_data), (
            "All items should be assigned to a cluster"
        )

    def test_agglomerative_clustering(self, cluster_operator, sample_clustering_data):
        """Test Agglomerative clustering with video modality."""
        n_clusters = 2
        modality = "video"

        result = cluster_operator.run(
            sample_clustering_data, n_clusters=n_clusters, modality=modality
        )

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert len(result) == n_clusters, f"Should have {n_clusters} clusters"

        # All other checks are similar to KMeans test
        all_items = []
        for key, cluster_items in result.items():
            assert key.startswith("cluster_"), (
                "Cluster keys should start with 'cluster_'"
            )
            assert isinstance(cluster_items, list), "Cluster values should be lists"
            all_items.extend(cluster_items)

        assert len(all_items) == len(sample_clustering_data), (
            "All items should be assigned to a cluster"
        )


class TestIntegration:
    """Test integration between video vector generation and clustering."""

    def test_video_to_clusters_integration(
        self, video_operator, cluster_operator, test_video_url, expected_vector_dim
    ):
        """Test integration between video vector generation and clustering."""
        # Generate video vectors
        video_obj = VideoFactory.make_from_url(test_video_url)
        assert video_obj is not None, "Video object should be successfully created"

        video_vec_generator = video_operator.run(video_obj)
        first_vec = next(video_vec_generator)
        avg_vector = first_vec["vid_vec"]

        # Collect I-frame vectors as well (up to 5)
        i_frame_vectors = []
        for i, vec_data in enumerate(video_vec_generator):
            if i >= 5:  # Limit to 5 I-frames to keep test reasonable
                break
            i_frame_vectors.append(vec_data["vid_vec"])

        # Prepare data for clustering
        clustering_data = [
            {"embedding": avg_vector, "payload": {"id": "avg_frame", "type": "average"}}
        ]

        for i, vec in enumerate(i_frame_vectors):
            clustering_data.append({
                "embedding": vec,
                "payload": {"id": f"iframe_{i}", "type": "iframe"},
            })

        # Cluster the vectors
        n_clusters = 2  # Arbitrary, just to demonstrate
        modality = "video"

        result = cluster_operator.run(
            clustering_data, n_clusters=n_clusters, modality=modality
        )

        # Verify clustering results
        assert 1 <= len(result) <= n_clusters, (
            f"Should have between 1 and {n_clusters} clusters"
        )

        # All items should be in clusters
        all_items = []
        for cluster_items in result.values():
            all_items.extend(cluster_items)
        assert len(all_items) == len(clustering_data), (
            "All items should be assigned to a cluster"
        )

    def test_full_pipeline(
        self, video_operator, cluster_operator, test_video_url, expected_vector_dim
    ):
        """Test the full pipeline with video vector extraction and clustering."""
        # 1. Generate video vector
        video_obj = VideoFactory.make_from_url(test_video_url)
        video_vec_generator = video_operator.run(video_obj)
        video_avg_vec = next(video_vec_generator)["vid_vec"]

        # Collect some I-frame vectors
        iframe_vectors = []
        for i, vec_data in enumerate(video_vec_generator):
            if i >= 4:  # Just get a few frames
                break
            iframe_vectors.append(vec_data["vid_vec"])

        # 2. Prepare data for clustering
        clustering_data = [
            {
                "embedding": video_avg_vec,
                "payload": {"id": "avg_vector", "type": "video_avg"},
            }
        ]

        # Add I-frame vectors
        for i, vec in enumerate(iframe_vectors):
            clustering_data.append({
                "embedding": vec,
                "payload": {"id": f"iframe_{i}", "type": "video_iframe"},
            })

        # Add some synthetic vectors to ensure meaningful clustering
        for i in range(3):
            clustering_data.append({
                "embedding": [float(10 * (i + 1))] * expected_vector_dim,
                "payload": {"id": f"synthetic_{i}", "type": "synthetic"},
            })

        # 3. Cluster the vectors
        n_clusters = 3  # Expect video frames in one cluster, synthetic in another
        modality = "video"

        cluster_result = cluster_operator.run(
            clustering_data, n_clusters=n_clusters, modality=modality
        )

        # 4. Verify results
        assert 1 <= len(cluster_result) <= n_clusters, (
            f"Should have between 1 and {n_clusters} clusters"
        )

        # All items should be in clusters
        all_items = []
        for cluster_items in cluster_result.values():
            all_items.extend(cluster_items)
        assert len(all_items) == len(clustering_data), (
            "All items should be assigned to a cluster"
        )


@pytest.fixture(scope="session", autouse=True)
def cleanup_operators(video_operator, cluster_operator):
    """Cleanup operators after each test."""
    yield
    video_operator.cleanup()
    cluster_operator.cleanup()
