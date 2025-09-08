from benchmark.config import BENCHMARK_VIDEOS
from benchmark.profiler import Profiler
from feluda.factory import VideoFactory
from operators.vid_vec_rep import VidVecRep


def benchmark() -> list[dict]:
    """Benchmark the VidVecRep operator."""
    test_data = [
        {"file": VideoFactory.make_from_file_on_disk(video_path)}
        for video_path in BENCHMARK_VIDEOS
    ]
    results = []

    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=VidVecRep,
            operator_name="vid_vec_rep",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
