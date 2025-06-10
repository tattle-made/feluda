"""Operator to extract video vector representations using CLIP-ViT-B-32."""


def initialize(param: dict = None) -> None:
    """Initialize the operator.

    Args:
        param (dict): Parameters for initialization
    """
    print("Installing packages for vid_vec_rep_clip")
    global os, VideoAnalyzer, gendata

    # Imports
    import os
    import subprocess
    import tempfile
    from typing import Generator

    import torch
    from PIL import Image
    from transformers import AutoProcessor, CLIPModel

    # Load the model and processor
    processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

    # Set the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    class VideoAnalyzer:
        """A class for video feature extraction."""

        def __init__(self, fname: str) -> None:
            """Initialize the `VideoAnalyzer` class.

            Args:
                fname (str): Path to the video file
            """
            self.model = model
            self.device = device
            self.frame_images = []
            self.feature_matrix = []
            self.fname = fname
            self.analyze(fname)

        def get_mean_feature(self) -> torch.Tensor:
            """Compute the mean feature vector from the feature matrix.

            Returns:
                torch.Tensor: Mean feature vector
            """
            return torch.mean(self.feature_matrix, dim=0)

        def analyze(self) -> None:
            """Analyze the video file and extract features.

            Args:
                fname (str): Path to the video file
            """
            # check if file exists
            if not os.path.exists(self.fname):
                raise FileNotFoundError(f"File not found: {self.fname}")

            # Extract I-frames and features
            self.frame_images = self.extract_frames(self.fname)
            self.feature_matrix = self.extract_features(self.frame_images)

        def extract_frames(self) -> list:
            """Extract I-frames from the video file using `ffmpeg`.

            Args:
                fname (str): Path to the video file

            Returns:
                list: List of PIL Images
            """
            with tempfile.TemporaryDirectory() as temp_dir:
                # Command to extract I-frames using ffmpeg's command line tool
                cmd = rf"""
                ffmpeg -i "{self.fname}" -vf "select=eq(pict_type\,I)" -vsync vfr "{temp_dir}/frame_%05d.jpg"
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
            inputs = processor(
                images=images, return_tensors="pt", padding=True, truncation=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}  # move to device
            with torch.no_grad():
                features = self.model.get_image_features(**inputs)
                return features

    def gendata(vid_analyzer: VideoAnalyzer) -> Generator[dict, None, None]:
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
            "vid_vec": vid_analyzer.get_mean_feature().tolist(),
            "is_avg": True,
        }
        # I-frame vectors
        for keyframe in vid_analyzer.feature_matrix:
            yield {
                "vid_vec": keyframe.tolist(),
                "is_avg": False,
            }


def run(file) -> dict:
    """Run the operator.

    Args:
        file (dict): `VideoFactory` file object

    Returns:
        generator: Yields video and I-frame vector representations
    """
    fname = file["path"]
    try:
        vid_analyzer = VideoAnalyzer(fname)
        return gendata(vid_analyzer)
    finally:
        os.remove(fname)


def cleanup() -> None:
    """Cleanup the operator."""


def state() -> dict:
    """Get the state of the operator.

    Returns:
        dict: State of the operator
    """
