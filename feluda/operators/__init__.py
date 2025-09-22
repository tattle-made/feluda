from typing import Any

from feluda.operator import Operator


def lazy_import(module_name: str) -> Any:
    class_name = "".join(word.capitalize() for word in module_name.split("_"))

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


ClassifyVideoZeroShot = lazy_import("classify_video_zero_shot")
ClusterEmbeddings = lazy_import("cluster_embeddings")
DetectLewdImages = lazy_import("detect_lewd_images")
DetectTextInImage = lazy_import("detect_text_in_image")
DimensionReduction = lazy_import("dimension_reduction")
ImageVecRep = lazy_import("image_vec_rep")
VidVecRep = lazy_import("vid_vec_rep")
VideoHash = lazy_import("video_hash")

__all__ = [
    "ClassifyVideoZeroShot",
    "ClusterEmbeddings",
    "DetectLewdImages",
    "DetectTextInImage",
    "DimensionReduction",
    "ImageVecRep",
    "VidVecRep",
    "VideoHash",
]
