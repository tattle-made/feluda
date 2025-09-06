from benchmark.config import BENCHMARK_VIDEOS
from benchmark.profiler import Profiler
from feluda.factory import VideoFactory
from operators.classify_video_zero_shot import ClassifyVideoZeroShot


def benchmark() -> list[dict]:
    """Benchmark the ClassifyVideoZeroShot operator."""
    test_data = [
        {"file": VideoFactory.make_from_file_on_disk(video_path)}
        for video_path in BENCHMARK_VIDEOS
    ]
    results = []
    for test_item in test_data:
        print(test_item)
        result = Profiler.benchmark_operator(
            operator_class=ClassifyVideoZeroShot,
            operator_name="video_classifier",
            runtime_kwargs=test_item,
        )
        results.append(result)
    return results
