# Cluster Embeddings Operator

## Description

The `Cluster Embeddings` operator clusters high-dimensional embeddings into groups using KMeans, Agglomerative Clustering, or Affinity Propagation algorithms from scikit-learn. It supports both audio and video modalities, and can automatically determine the number of clusters using Affinity Propagation if not specified.

## Model Information

- **KMeans**: Partitions data into a specified number of clusters by minimizing within-cluster variance.
- **Agglomerative Clustering**: Hierarchical clustering that merges pairs of clusters based on distance.
- **Affinity Propagation**: Clusters data by sending messages between points, automatically determining the number of clusters.
- **Vector Size**: Any dimensionality supported by scikit-learn clustering algorithms.
- **Usage**: Groups similar embeddings for downstream tasks such as retrieval, summarization, or visualization.

## Dependencies

- scikit-learn >= 1.6.1
- numpy >= 1.26,<2.2.0

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/cluster_embeddings"
   uv pip install "feluda[dev]"
   ```

3. Run the tests:

   ```bash
   pytest operators/cluster_embeddings/test.py
   ```

## Usage

```python
from operators.cluster_embeddings import ClusterEmbeddings

# Initialize the operator
operator = ClusterEmbeddings()

# Prepare input data
input_data = [
    {"payload": "A", "embedding": [0, 1]},
    {"payload": "B", "embedding": [1, 0]},
    {"payload": "C", "embedding": [100, 101]},
    {"payload": "D", "embedding": [101, 100]},
]

# Run clustering (audio modality, KMeans)
result = operator.run(input_data, n_clusters=2, modality="audio")
print(result)

# Run clustering (video modality, Agglomerative)
result = operator.run(input_data, n_clusters=2, modality="video")
print(result)

# Run clustering with automatic cluster count (Affinity Propagation)
result = operator.run(input_data, modality="audio")
print(result)
```
