from benchmark.config import BENCHMARK_VIDEOS
from benchmark.profiler import Profiler
from operators.video_hash import VideoHash


def benchmark() -> list[dict]:
    """Benchmark the VideoHash operator."""
    test_data = [{"video_path": video_path} for video_path in BENCHMARK_VIDEOS]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=VideoHash,
            operator_name="video_hash",
            runtime_kwargs=test_item,
        )
        results.append(result)
    return results
