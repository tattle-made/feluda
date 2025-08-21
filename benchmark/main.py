# Import benchmark modules
from benchmark.operators import (
    classify_video_zero_shot,
    cluster_embeddings,
    detect_lewd_images,
    detect_text_in_image_tesseract,
    dimension_reduction,
    image_vec_rep_resnet,
    vid_vec_rep_clip,
    video_hash_tmk,
)
from benchmark.report import BenchmarkReport


def main():
    report = BenchmarkReport()

    # List of benchmark modules to run
    benchmark_modules = [
        ("vid_vec_rep_clip", vid_vec_rep_clip),
        ("video_hash_tmk", video_hash_tmk),
        ("image_vec_rep_resnet", image_vec_rep_resnet),
        ("detect_text_in_image_tesseract", detect_text_in_image_tesseract),
        ("detect_lewd_images", detect_lewd_images),
        ("classify_video_zero_shot", classify_video_zero_shot),
        ("dimension_reduction", dimension_reduction),
        ("cluster_embeddings", cluster_embeddings),
    ]

    for name, module in benchmark_modules:
        print(f"\n=== Benchmarking {name} ===")
        results = module.benchmark()
        for result in results:
            report.add(result)

    report.save_json()
    report.save_markdown()


if __name__ == "__main__":
    main()


import operators
for op in operators.__all__:
    print(f"Loaded operator: {op}")