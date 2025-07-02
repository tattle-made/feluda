import contextlib
import gc
import os
import shutil
import subprocess
import tempfile
from typing import Generator

import torch
from PIL import Image
from transformers import AutoProcessor, CLIPModel

from feluda import BaseOperator
from feluda.factory import VideoFactory


class VidVecRepClip(BaseOperator):
    """Operator to extract video vector representations using CLIP-ViT-B-32."""

    def __init__(self) -> None:
        """Initialize the `VidVecRepClip` class."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.frame_images = []
        self.feature_matrix = []
        self.load_model()
        self.validate_system()

    def load_model(self) -> None:
        """Load the CLIP model and processor onto the specified device."""
        try:
            self.processor = AutoProcessor.from_pretrained(
                "openai/clip-vit-base-patch32"
            )
            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        except Exception as e:
            raise RuntimeError(
                f"Failed to load the CLIP model or processor: {e!s} "
            ) from e
        self.model.to(self.device)

    @staticmethod
    def validate_system() -> None:
        """Validate that required system dependencies are available.

        Checks if FFmpeg is installed and accessible in the system PATH.
        """
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "FFmpeg is not installed or not found in system PATH. "
                "Please install FFmpeg to use this operator."
            )

    def get_mean_feature(self) -> torch.Tensor:
        """Compute the mean feature vector from the feature matrix.

        Returns:
            torch.Tensor: Mean feature vector
        """
        if self.feature_matrix is None or len(self.feature_matrix) == 0:
            raise ValueError("Feature matrix is empty. Please analyze a video first.")
        return torch.mean(self.feature_matrix, dim=0)

    def analyze(self, fname: str) -> None:
        """Analyze the video file and extract features.

        Args:
            fname (str): Path to the video file
        """
        self.frame_images = self.extract_frames(fname)

        if not self.frame_images:
            raise ValueError(f"No frames could be extracted from: {fname!s}")
        self.feature_matrix = self.extract_features(self.frame_images)

    @staticmethod
    def extract_frames(fname: str) -> list[Image.Image]:
        """Extract I-frames from the video file using `ffmpeg`.

        Args:
            fname (str): Path to the video file

        Returns:
            list: List of PIL Images
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Command to extract I-frames using ffmpeg
            cmd = [
                "ffmpeg",
                "-i",
                fname,
                "-vf",
                "select=eq(pict_type\\,I)",
                "-vsync",
                "vfr",
                "-y",
                os.path.join(temp_dir, "frame_%05d.jpg"),
            ]

            try:
                subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=300,  # 5 minute timeout
                )
                # print("FFmpeg stdout:", result.stdout)
                # print("FFmpeg stderr:", result.stderr)
            except subprocess.TimeoutExpired:
                raise TimeoutError(f"FFmpeg timed out while processing: {fname}")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"FFmpeg failed to extract frames from {fname}: {e.stderr}"
                    f"Stdout: {e.stdout}\n"
                    f"Stderr: {e.stderr}"
                ) from e

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
        if not images:
            raise ValueError("Images list cannot be empty")
        inputs = self.processor(
            images=images, return_tensors="pt", padding=True, truncation=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}  # move to device
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
            return features

    def gendata(self) -> Generator[dict, None, None]:
        """Yield video vector representations from the `VidVecRepClip` prototype.

        Yields:
            dict: A dictionary containing:
                - `vid_vec` (list): Vector representation
                - `is_avg` (bool): A flag indicating whether the vector is the average vector or a I-frame vector
        """
        if self.feature_matrix is None or len(self.feature_matrix) == 0:
            raise ValueError("Feature matrix is empty. Please analyze a video first.")
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

    def run(
        self, file: VideoFactory, remove_after_processing: bool = False
    ) -> Generator[dict, None, None]:
        """Run the operator.

        Args:
            file (dict): `VideoFactory` file object
            remove_after_processing (bool): Whether to remove the file after processing

        Returns:
            generator: Yields video and I-frame vector representations
        """
        if not isinstance(file, dict) or "path" not in file:
            raise ValueError(
                "Invalid file object. Expected VideoFactory object with 'path' key."
            )
        fname = file["path"]

        if not os.path.exists(fname):
            raise FileNotFoundError(f"File not found: {fname}")

        try:
            self.analyze(fname)
            return self.gendata()
        finally:
            if remove_after_processing:
                with contextlib.suppress(FileNotFoundError):
                    os.remove(fname)

    def cleanup(self) -> None:
        """Cleanup the operator."""
        del self.model
        del self.processor

        self.frame_images.clear()
        self.feature_matrix.clear()

        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def state(self) -> dict:
        """Get the state of the operator.

        Returns:
            dict: State of the operator
        """
        return {
            "device": self.device,
            "model": self.model,
            "processor": self.processor,
            "frame_images": self.frame_images.copy(),
            "feature_matrix": self.feature_matrix.copy() if self.feature_matrix else [],
        }
