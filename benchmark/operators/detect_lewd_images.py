from benchmark.profiler import Profiler
from operators.detect_lewd_images import LewdImageDetector


def benchmark():
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

        if result["status"] == "success":
            print(
                f"  Time: {result['execution']['execution_time_seconds']:.2f}s, "
                f"Memory: {result['execution']['memory_change_mb']:.2f}MB"
            )
        else:
            print(f"  Failed: {result.get('error', 'Unknown error')}")

    return results
