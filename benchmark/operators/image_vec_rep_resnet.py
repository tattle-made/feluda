from benchmark.config import BENCHMARK_IMAGES
from benchmark.profiler import Profiler
from feluda.factory import ImageFactory
from operators.image_vec_rep_resnet import ImageVecRepResnet


def benchmark() -> list[dict]:
    """Benchmark the ImageVecRepResnet operator."""
    test_data = [
        {"image": ImageFactory.make_from_file_on_disk_to_path(image)}
        for image in BENCHMARK_IMAGES
    ]

    results = []
    for test_item in test_data:
        result = Profiler.benchmark_operator(
            operator_class=ImageVecRepResnet,
            operator_name="image_vec_rep_resnet",
            runtime_kwargs=test_item,
        )
        results.append(result)

    return results
