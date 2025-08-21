from benchmark.profiler import Profiler
from operators.image_vec_rep_resnet import ImageVecRepResnet


def benchmark() -> list[dict]:
    """Benchmark the ImageVecRepResnet operator."""
    test_data = [
        {"file": "test_images/image1.jpg"},
        {"file": "test_images/image2.png"},
    ]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=ImageVecRepResnet,
            operator_name="image_vec_rep_resnet",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
