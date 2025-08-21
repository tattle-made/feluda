from benchmark.profiler import Profiler
from operators.video_hash_tmk import VideoHashTmk


def benchmark() -> list[dict]:
    """Benchmark the VideoHashTmk operator."""
    test_data = [
        {"file": "test_videos/video1.mp4"},
        {"file": "test_videos/video2.mp4"},
    ]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=VideoHashTmk,
            operator_name="video_hash_tmk",
            runtime_kwargs=test_item,
        )
        results.append(result)
    return results
