from benchmark.profiler import Profiler
from operators.detect_text_in_image_tesseract import ImageTextDetector


def benchmark() -> list[dict]:
    """Benchmark the ImageTextDetector operator."""
    test_data = [
        {"file": "test_images/image1.jpg"},
        {"file": "test_images/image2.png"},
    ]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=ImageTextDetector,
            operator_name="detect_text_in_image_tesseract",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
