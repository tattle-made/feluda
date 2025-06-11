import gc
import os
import subprocess
import tempfile
from typing import Generator

import torch
from PIL import Image
from transformers import AutoProcessor, CLIPModel

"""Operator to extract video vector representations using CLIP-ViT-B-32."""

_analyzer = None


class VideoAnalyzer:
    """A class for video feature extraction."""

    def __init__(self) -> None:
        """Initialize the `VideoAnalyzer` class."""
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.frame_images = []
        self.feature_matrix = []

    def get_mean_feature(self) -> torch.Tensor:
        """Compute the mean feature vector from the feature matrix.

        Returns:
            torch.Tensor: Mean feature vector
        """
        return torch.mean(self.feature_matrix, dim=0)

    def analyze(self, fname: str) -> None:
        """Analyze the video file and extract features.

        Args:
            fname (str): Path to the video file
        """
        self.frame_images = self.extract_frames(fname)
        self.feature_matrix = self.extract_features(self.frame_images)

    @staticmethod
    def extract_frames(fname: str) -> list:
        """Extract I-frames from the video file using `ffmpeg`.

        Args:
            fname (str): Path to the video file

        Returns:
            list: List of PIL Images
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Command to extract I-frames using ffmpeg's command line tool
            cmd = rf"""
            ffmpeg -i "{fname}" -vf "select=eq(pict_type\,I)" -vsync vfr "{temp_dir}/frame_%05d.jpg"
            """
            with subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as process:
                process.wait()
            frames = []
            for filename in os.listdir(temp_dir):
                if filename.endswith(".jpg"):
                    image_path = os.path.join(temp_dir, filename)
                    with Image.open(image_path) as img:
                        frames.append(img.copy())
            return frames

    def extract_features(self, images: list) -> torch.Tensor:
        """Extract features from a list of images using pre-trained CLIP-ViT-B-32.

        Args:
            images (list): List of PIL Images

        Returns:
            torch.Tensor: Feature matrix of shape (batch, 512)
        """
        inputs = self.processor(
            images=images, return_tensors="pt", padding=True, truncation=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}  # move to device
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
            return features

    def gendata(self) -> Generator[dict, None, None]:
        """Yield video vector representations from the `VideoAnalyzer` prototype.

        Args:
            vid_analyzer (VideoAnalyzer): `VideoAnalyzer` instance

        Yields:
            dict: A dictionary containing:
                - `vid_vec` (list): Vector representation
                - `is_avg` (bool): A flag indicating whether the vector is the average vector or a I-frame vector
        """
        # average vector
        yield {
            "vid_vec": self.get_mean_feature().tolist(),
            "is_avg": True,
        }
        # I-frame vectors
        for keyframe in self.feature_matrix:
            yield {
                "vid_vec": keyframe.tolist(),
                "is_avg": False,
            }


def initialize(param: dict = None) -> None:
    """Initialize the operator.

    Args:
        param (dict): Parameters for initialization
    """
    global _analyzer

    _analyzer = VideoAnalyzer()


def run(file) -> dict:
    """Run the operator.

    Args:
        file (dict): `VideoFactory` file object

    Returns:
        generator: Yields video and I-frame vector representations
    """
    fname = file["path"]

    if not os.path.exists(fname):
        raise FileNotFoundError(f"File not found: {fname}")

    try:
        _analyzer.analyze(fname)
        return _analyzer.gendata()
    finally:
        os.remove(fname)


def cleanup() -> None:
    """Cleanup the operator."""
    global _analyzer

    del _analyzer
    gc.collect()
    torch.cuda.empty_cache()


def state() -> dict:
    """Get the state of the operator.

    Returns:
        dict: State of the operator
    """
    return {
        "analyzer": _analyzer,
        "device": _analyzer.device,
        "model": _analyzer.model,
        "processor": _analyzer.processor,
        "frame_images": _analyzer.frame_images,
        "feature_matrix": _analyzer.feature_matrix,
    }
