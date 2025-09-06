from benchmark.config import BENCHMARK_IMAGES
from benchmark.profiler import Profiler
from operators.detect_text_in_image import DetectTextInImage


def benchmark() -> list[dict]:
    """Benchmark the DetectTextInImage operator."""
    test_data = [{"file": image} for image in BENCHMARK_IMAGES]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=DetectTextInImage,
            operator_name="detect_text_in_image",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
