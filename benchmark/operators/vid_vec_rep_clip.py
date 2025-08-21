from benchmark.profiler import Profiler
from operators.vid_vec_rep_clip import VidVecRepClip


def benchmark() -> list[dict]:
    """Benchmark the VidVecRepClip operator."""
    test_data = [
        {"file": "test_videos/video1.mp4"},
        {"file": "test_videos/video2.mp4"},
    ]

    results = []

    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=VidVecRepClip,
            operator_name="vid_vec_rep_clip",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
