import random

from benchmark.data_generator import DataGenerator
from benchmark.profiler import Profiler
from operators.dimension_reduction import DimensionReduction


def benchmark() -> list[dict]:
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

        # Test with different reduction methods (only supported ones)
        for method in ["tsne", "umap"]:
            # Convert embeddings to the format expected by the operator
            runtime_kwargs = {
                "input_data": [
                    {"payload": f"sample_{i}", "embedding": embedding.tolist()}
                    for i, embedding in enumerate(embeddings)
                ],
            }

            operator_kwargs = {
                "model_type": method,
                "params": {
                    "n_components": random.randint(2, 3),
                },
            }

            result = Profiler.benchmark_operator(
                operator_class=DimensionReduction,
                operator_name=f"dimension_reduction_{method}",
                runtime_kwargs=runtime_kwargs,
                operator_kwargs=operator_kwargs,
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
