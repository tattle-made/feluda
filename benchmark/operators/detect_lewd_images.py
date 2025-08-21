from benchmark.profiler import Profiler
from operators.detect_lewd_images import LewdImageDetector


def benchmark() -> list[dict]:
    """Benchmark the LewdImageDetector operator."""
    test_data = [
        {"file": "test_images/image1.jpg"},
        {"file": "test_images/image2.png"},
    ]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=LewdImageDetector,
            operator_name="detect_lewd_images",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
