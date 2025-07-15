import pytest

from operators.cluster_embeddings import ClusterEmbeddings

MOCK_DATA = [
    {"payload": "A", "embedding": [0, 1]},
    {"payload": "B", "embedding": [1, 0]},
    {"payload": "C", "embedding": [100, 101]},
    {"payload": "D", "embedding": [101, 100]},
]
EXPECTED_CLUSTERS = [["A", "B"], ["C", "D"]]


@pytest.fixture(scope="module")
def operator():
    return ClusterEmbeddings()


def test_kmeans_audio(operator):
    result = operator.run(MOCK_DATA, n_clusters=2, modality="audio")
    assert "cluster_0" in result
    assert "cluster_1" in result
    assert len(result) == 2
    assert sorted([sorted(result["cluster_0"]), sorted(result["cluster_1"])]) == sorted([
        sorted(cluster) for cluster in EXPECTED_CLUSTERS
    ])


def test_agglomerative_video(operator):
    result = operator.run(MOCK_DATA, n_clusters=2, modality="video")
    assert "cluster_0" in result
    assert "cluster_1" in result
    assert len(result) == 2
    assert sorted([sorted(result["cluster_0"]), sorted(result["cluster_1"])]) == sorted([
        sorted(cluster) for cluster in EXPECTED_CLUSTERS
    ])


def test_affinity_propagation(operator):
    result = operator.run(MOCK_DATA, modality="audio")
    assert "cluster_0" in result
    assert "cluster_1" in result
    assert len(result) == 2
    assert sorted([sorted(result["cluster_0"]), sorted(result["cluster_1"])]) == sorted([
        sorted(cluster) for cluster in EXPECTED_CLUSTERS
    ])


def test_missing_modality(operator):
    with pytest.raises(ValueError) as excinfo:
        operator.run(MOCK_DATA, n_clusters=2)
    assert "Modality must be specified" in str(excinfo.value)


def test_invalid_modality(operator):
    with pytest.raises(ValueError):
        operator.run(MOCK_DATA, n_clusters=2, modality="text")


def test_input_data_not_list(operator):
    with pytest.raises(ValueError):
        operator.run("notalist", n_clusters=2, modality="audio")


def test_input_data_empty(operator):
    with pytest.raises(ValueError):
        operator.run([], n_clusters=2, modality="audio")


def test_missing_embedding_key(operator):
    bad_data = [{"payload": "A"}]
    with pytest.raises(KeyError):
        operator.run(bad_data, n_clusters=1, modality="audio")


def test_missing_payload_key(operator):
    bad_data = [{"embedding": [0, 1]}]
    with pytest.raises(KeyError):
        operator.run(bad_data, n_clusters=1, modality="audio")


def test_n_clusters_not_int(operator):
    with pytest.raises(ValueError):
        operator.run(MOCK_DATA, n_clusters="two", modality="audio")


def test_embedding_not_list_of_numbers(operator):
    bad_data = [{"payload": "A", "embedding": ["x", "y"]}]
    with pytest.raises(Exception):
        operator.run(bad_data, n_clusters=1, modality="audio")
