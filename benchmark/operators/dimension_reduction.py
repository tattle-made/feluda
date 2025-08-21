from benchmark.data_generator import DataGenerator
from benchmark.profiler import Profiler
from operators.dimension_reduction import DimensionReduction


def benchmark():
    """Benchmark the DimensionReduction operator."""
    results = []

    # Generate test embeddings
    test_datasets = {
        "small_500x512": DataGenerator.generate_embeddings(500, 512),
        "medium_2000x512": DataGenerator.generate_embeddings(2000, 512),
        "large_5000x512": DataGenerator.generate_embeddings(5000, 512),
        "xlarge_10000x512": DataGenerator.generate_embeddings(10000, 512),
    }

    for dataset_name, embeddings in test_datasets.items():
        print(f"Processing: {dataset_name} (shape: {embeddings.shape})")

        # Test with different reduction methods
        for method in ["tsne", "pca", "umap"]:
            runtime_kwargs = {
                "embeddings": embeddings,
                "method": method,
                "n_components": 2,
            }

            result = Profiler.benchmark_operator(
                operator_class=DimensionReduction,
                operator_name=f"dimension_reduction_{method}",
                runtime_kwargs=runtime_kwargs,
            )

            # Add dataset info to result
            result["data_description"] = f"{dataset_name} - {method}"
            if result["status"] == "success" and "output_info" not in result:
                result["output_info"] = {
                    "method": method,
                    "input_shape": embeddings.shape,
                }

            results.append(result)

    return results
