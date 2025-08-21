from benchmark.profiler import Profiler
from operators.classify_video_zero_shot import VideoClassifier


def benchmark() -> list[dict]:
    """Benchmark the VideoClassifier operator."""
    test_data = [
        {"file": "test/image1.jpg", "labels": ["label1", "label2"]},
        {"file": "test/image2.jpg", "labels": ["label1", "label3"]},
    ]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=VideoClassifier,
            operator_name="video_classifier",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
