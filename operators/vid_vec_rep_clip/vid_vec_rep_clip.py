"""
Operator to extract video vector representations using CLIP-ViT-B-32.
"""

import time
import platform
def initialize(param):
    """
    Initializes the operator.

    Args:
        param (dict): Parameters for initialization
    """
    print("Installing packages for vid_vec_rep_clip")
    global os
    global VideoAnalyzer, gendata

    # Imports
    import os
    import subprocess
    import tempfile
    import torch
    from PIL import Image
    from transformers import AutoProcessor, CLIPModel

    # Load the model and processor
    processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

    # Set the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    def gendata(vid_analyzer):
        """
        Yields video vector representations from a `VideoAnalyzer` prototype.

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

    class VideoAnalyzer:
        """
        A class for video feature extraction.
        """

        def __init__(self, fname, frame_sample_rate=1):
            """
            Constructor for the `VideoAnalyzer` class.

            Args:
                fname (str): Path to the video file
                frame_sample_rate (int): Sample every Nth I-frame
            """
            self.model = model
            self.device = device
            self.processor = processor
            self.frame_sample_rate = frame_sample_rate

            self.fname = fname
            self.feature_matrix = []
            self.analyze(fname)

        def get_mean_feature(self):
            """
            Returns:
                torch.Tensor: Mean feature vector
            """
            return torch.mean(self.feature_matrix, dim=0)

        def analyze(self, fname):
            """
            Analyzes the video file and extracts features.

            Args:
                fname (str): Path to the video file

            Raises:
                FileNotFoundError: If the file is not found
            """
            if not os.path.exists(fname):
                raise FileNotFoundError(f"File not found: {fname}")

            print(f"Analyzing video: {fname}")           
            self.feature_matrix = self.extract_features_streaming(fname)           

        def extract_features_streaming(self, fname):
            feature_list = []
            with tempfile.TemporaryDirectory() as temp_dir:   
                cmd = [
                    "ffmpeg",
                    "-i", fname,
                    "-vf", "select=eq(pict_type\\,I)",
                    "-vsync", "vfr",
                    f"{temp_dir}/frame_%05d.jpg"
                ]            
                print("Extracting I-frames with ffmpeg...")
                subprocess.run(
                    cmd,
                    check=True,
                    stdout=subprocess.PIPE,  
                    stderr=subprocess.PIPE   
                )
               
                filenames = sorted([f for f in os.listdir(temp_dir) if f.endswith(".jpg")])
                print(f"Total I-frames found: {len(filenames)}")
                print(f"Sampling every {self.frame_sample_rate}th frame")

                for i, filename in enumerate(filenames):
                    if i % self.frame_sample_rate != 0:
                        continue
                    image_path = os.path.join(temp_dir, filename)
                    with Image.open(image_path) as img:
                        img = img.convert("RGB")
                        feature = self.extract_single_feature(img)
                        feature_list.append(feature.cpu())

            return torch.stack(feature_list)

        def extract_single_feature(self, img):
            inputs = self.processor(images=img, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                feature = self.model.get_image_features(**inputs)
            return feature.squeeze(0)

def run(file):
    fname = file["path"]

    try:
        vid_analyzer = VideoAnalyzer(fname, frame_sample_rate=1)  # Now processing all I-frames
        return gendata(vid_analyzer)
    finally:
        if file.get("is_temp", False) and os.path.exists(fname):
            os.remove(fname)

def cleanup(param):
    pass

def state():
    pass

