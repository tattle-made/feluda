from benchmark.config import BENCHMARK_IMAGES
from benchmark.profiler import Profiler
from operators.detect_lewd_images import DetectLewdImages


def benchmark() -> list[dict]:
    """Benchmark the DetectLewdImages operator."""
    test_data = [{"file": image} for image in BENCHMARK_IMAGES]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=DetectLewdImages,
            operator_name="detect_lewd_images",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
