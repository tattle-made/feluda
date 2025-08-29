"""Configuration for benchmark videos and images."""

from pathlib import Path

from feluda.factory import ImageFactory

VIDEOS_DIR = Path(__file__).parent / "videos"
IMAGES_DIR = Path(__file__).parent / "images"
VIDEOS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


def get_benchmark_videos() -> list[str]:
    """Get all video files (with full paths) from the benchmark/videos directory."""
    if not VIDEOS_DIR.exists():
        return []

    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}

    return sorted(
        str(file_path)
        for file_path in VIDEOS_DIR.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in video_extensions
    )


BENCHMARK_VIDEOS = get_benchmark_videos()

BENCHMARK_IMAGE_URLS = [
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/hindi-text.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/tamil-text.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/telugu-text.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/text.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news1.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news2.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news3.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news4.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news5.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news6.png",
    "https://github.com/tattle-made/feluda_datasets/blob/main/feluda-sample-media/newspaper-clipings/news7.png",
]

BENCHMARK_IMAGE_URLS = [url.replace("blob", "raw") for url in BENCHMARK_IMAGE_URLS]


def get_benchmark_images() -> list[str]:
    """Download images only if they don't already exist."""
    images = []
    for url in BENCHMARK_IMAGE_URLS:
        filename = url.split("/")[-1]
        image_path = IMAGES_DIR / filename

        if not image_path.exists():
            obj = ImageFactory.make_from_url_to_path(url, str(image_path))
        else:
            obj = ImageFactory.make_from_file_on_disk_to_path(str(image_path))

        images.append(obj)
    return images


BENCHMARK_IMAGES = get_benchmark_images()
