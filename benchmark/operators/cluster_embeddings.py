from benchmark.data_generator import DataGenerator
from benchmark.profiler import Profiler
from operators.cluster_embeddings import ClusterEmbeddings


def benchmark():
    """Benchmark the ClusterEmbeddings operator."""
    results = []

    # Generate test embeddings with known clusters
    test_datasets = [
        (
            "clustered_3clusters",
            *DataGenerator.generate_embeddings_with_clusters(3, 300, 512),
        ),
        (
            "clustered_5clusters",
            *DataGenerator.generate_embeddings_with_clusters(5, 200, 512),
        ),
        (
            "clustered_10clusters",
            *DataGenerator.generate_embeddings_with_clusters(10, 100, 512),
        ),
    ]

    for dataset_name, embeddings, true_labels in test_datasets:
        print(f"Processing: {dataset_name} (shape: {embeddings.shape})")

        # Test with different clustering methods
        for method in ["kmeans", "dbscan", "agglomerative"]:
            runtime_kwargs = {
                "embeddings": embeddings,
                "method": method,
            }

            # For kmeans, specify the number of clusters
            if method == "kmeans":
                runtime_kwargs["n_clusters"] = len(set(true_labels))

            result = Profiler.benchmark_operator(
                operator_class=ClusterEmbeddings,
                operator_name=f"cluster_embeddings_{method}",
                runtime_kwargs=runtime_kwargs,
            )

            # Add dataset info to result
            result["data_description"] = f"{dataset_name} - {method}"
            if result["status"] == "success" and "output_info" not in result:
                result["output_info"] = {
                    "n_samples": len(embeddings),
                    "n_features": embeddings.shape[1],
                    "method": method,
                    "true_clusters": len(set(true_labels)),
                }

            results.append(result)
    return results
