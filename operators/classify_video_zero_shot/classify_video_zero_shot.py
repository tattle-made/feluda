import contextlib
import os
import shutil
import subprocess
import tempfile
from typing import Any

import torch
from PIL import Image
from transformers import AutoProcessor, CLIPModel

from feluda import Operator
from feluda.factory import VideoFactory


class VideoClassifier(Operator):
    """Operator to classify a video into given labels using CLIP-ViT-B-32 and a zero-shot approach."""

    def __init__(self) -> None:
        """Initialize the `VideoClassifier` operator, loads the CLIP model and processor, and validates system dependencies."""
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.validate_system()

        try:
            self.processor = AutoProcessor.from_pretrained(
                "openai/clip-vit-base-patch32"
            )
            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.model.to(self.device)
        except Exception as e:
            raise RuntimeError(f"Failed to load CLIP model or processor: {e}") from e

        self.labels: list[str] = []
        self.frame_images: list[Image.Image] = []
        self.probs: torch.Tensor | None = None

    @staticmethod
    def validate_system() -> None:
        """Validates that required system dependencies are available.
        (ffmpeg).
        """
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "FFmpeg is not installed or not found in system PATH. "
                "Please install FFmpeg to use this operator."
            )

    def gen_data(self) -> dict[str, Any]:
        """Generate output dict with prediction and probabilities.

        Returns:
            dict: A dictionary containing:
                - `prediction` (str): Predicted label
                - `probs` (list): Label probabilities
        """
        return {
            "prediction": self.labels[self.probs.argmax().item()],
            "probs": self.probs.tolist() if self.probs is not None else [],
        }

    def analyze(self) -> None:
        """Analyze the video file and generates predictions.

        Args:
            fname (str): Path to the video file
        """
        self.frame_images = self.extract_frames()
        if not self.frame_images:
            raise RuntimeError(
                "No frames extracted from video. Check if the video is valid."
            )
        self.probs = self.predict(self.frame_images, self.labels)

    def extract_frames(self) -> list[Image.Image]:
        """Extract I-frames from the video file using ffmpeg.

        Args:
            fname (str): Path to the video file
        Returns:
            list: List of PIL Images
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            cmd = [
                "ffmpeg",
                "-i",
                self.fname,
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
                    timeout=300,
                )
            except subprocess.TimeoutExpired:
                raise TimeoutError(f"FFmpeg timed out while processing: {self.fname}")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"FFmpeg failed to extract frames from {self.fname}: {e.stderr}\nStdout: {e.stdout}\nStderr: {e.stderr}"
                ) from e
            frames: list[Image.Image] = []
            for filename in os.listdir(temp_dir):
                if filename.endswith(".jpg"):
                    image_path = os.path.join(temp_dir, filename)
                    with Image.open(image_path) as img:
                        frames.append(img.copy())
            return frames

    def predict(self, images: list[Image.Image], labels: list[str]) -> torch.Tensor:
        """Run inference and gets label probabilities using a pre-trained
        CLIP-ViT-B-32.

        Args:
            images (list): List of PIL Images
            labels (list): List of labels
        Returns:
            torch.Tensor: Probability distribution across labels
        """
        if not images:
            raise ValueError("Image list for prediction must not be empty.")
        if not labels:
            raise ValueError("Label list for prediction must not be empty.")
        inputs = self.processor(
            text=labels,
            images=images,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            output = self.model(**inputs)
            logits_per_image = output.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            return probs.mean(dim=0)

    def run(
        self,
        file: VideoFactory,
        labels: list[str],
        remove_after_processing: bool = False,
    ) -> dict[str, Any]:
        """Run the operator.

        Args:
            file (dict): VideoFactory file object (must have a 'path' key)
            labels (list): List of labels
            remove_after_processing (bool): Whether to remove the file after processing
        Returns:
            dict: A dictionary containing prediction and probabilities
        """
        if not isinstance(file, dict) or "path" not in file:
            raise TypeError("file must be a dict with a 'path' key from VideoFactory.")
        if not isinstance(labels, list) or not all(isinstance(_, str) for _ in labels):
            raise TypeError("labels must be a list of strings.")
        if not labels:
            raise ValueError("Label list must not be empty.")

        fname = file["path"]
        self.fname = fname
        if not isinstance(fname, str) or not os.path.exists(fname):
            raise FileNotFoundError(f"File not found: {fname}")

        self.labels = labels
        self.analyze()

        try:
            return self.gen_data()
        finally:
            if remove_after_processing:
                with contextlib.suppress(FileNotFoundError):
                    os.remove(fname)

    def cleanup(self) -> None:
        """Clean up resources used by the operator."""
        self.frame_images.clear()
        self.probs = None
        self.labels.clear()

        del self.processor
        del self.model

    def state(self) -> dict[str, Any]:
        """Return the current state of the operator.

        Returns:
            dict: State of the operator
        """
        return {
            "labels": self.labels,
            "frame_images": [img.tobytes() for img in self.frame_images],
            "probs": self.probs.tolist() if self.probs is not None else [],
            "device": str(self.device),
            "model": self.model,
            "processor": self.processor,
        }
