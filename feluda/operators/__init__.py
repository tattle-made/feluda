from typing import Any

from feluda.operator import Operator


def lazy_import(module_name: str, class_name: str) -> Any:
    def _import() -> Any:
        try:
            module = __import__(module_name, fromlist=[class_name])
            return getattr(module, class_name)
        except ImportError as e:
            install_cmd = f"pip install {module_name.replace.replace('_', '-')}"
            raise ImportError(
                f"{class_name} operator is not installed. Run: {install_cmd}\nOriginal error: {e}"
            )

    class LazyLoader:
        def __getattr__(self, name: str) -> Any:
            cls = _import()
            return getattr(cls, name)

        def __call__(self, *args: Any, **kwargs: Any) -> Operator:
            cls = _import()
            return cls(*args, **kwargs)

    return LazyLoader()


VideoClassifier = lazy_import(
    "classify_video_zero_shot",
    "VideoClassifier",
)
ClusterEmbeddings = lazy_import(
    "cluster_embeddings",
    "ClusterEmbeddings",
)
LewdImageDetector = lazy_import(
    "detect_lewd_images",
    "LewdImageDetector",
)
ImageTextDetector = lazy_import(
    "detect_text_in_image_tesseract",
    "ImageTextDetector",
)
DimensionReduction = lazy_import(
    "dimension_reduction",
    "DimensionReduction",
)
ImageVecRepResnet = lazy_import(
    "image_vec_rep_resnet",
    "ImageVecRepResnet",
)
VidVecRepClip = lazy_import(
    "vid_vec_rep_clip",
    "VidVecRepClip",
)
VideoHashTmk = lazy_import(
    "video_hash_tmk",
    "VideoHashTmk",
)

__all__ = [
    "ClusterEmbeddings",
    "DimensionReduction",
    "ImageTextDetector",
    "ImageVecRepResnet",
    "LewdImageDetector",
    "VidVecRepClip",
    "VideoClassifier",
    "VideoHashTmk",
]
