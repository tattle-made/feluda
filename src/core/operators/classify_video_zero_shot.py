"""
Operator to classify a video into given labels using CLIP-ViT-B-32 and a zero-shot approach.
"""

def initialize(param):
    """
    Initializes the operator.

    Args:
        param (dict): Parameters for initialization
    """
    print("Installing packages for classify_video_zero_shot")
    global os
    global VideoClassifier, gendata

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
        Generates output dict with prediction and probabilities.

        Args:
            vid_analyzer (VideoClassifier): `VideoClassifier` instance

        Returns:
            dict: A dictionary containing:
                - `prediction` (str): Predicted label
                - `probs` (list): Label probabilities
        """
        return {
            "prediction": vid_analyzer.getPredictedLabel(),
            "probs": vid_analyzer.probs.tolist(),
        }

    class VideoClassifier:
        """
        A class for video classification.
        """
        def __init__(self, fname, labels):
            """
            Constructor for the `VideoClassifier` class.

            Args:
                fname (str): Path to the video file
                labels (list): List of labels
            """
            self.model = model
            self.device = device
            self.labels = labels
            self.frame_images = []
            self.feature_matrix = []
            self.analyze(fname)

        def analyze(self, fname):
            """
            Analyzes the video file and generates predictions.

            Args:
                fname (str): Path to the video file

            Raises:
                FileNotFoundError: If the file is not found
            """
            # check if file exists
            if not os.path.exists(fname):
                raise FileNotFoundError(f"File not found: {fname}")

            # Extract I-frames and features
            self.frame_images = self.extract_frames(fname)
            self.probs = self.predict(self.frame_images, self.labels)

        def extract_frames(self, fname):
            """
            Extracts I-frames from the video file using `ffmpeg`.

            Args:
                fname (str): Path to the video file

            Returns:
                list: List of PIL Images
            """
            with tempfile.TemporaryDirectory() as temp_dir:
                # Command to extract I-frames using ffmpeg's command line tool
                cmd=f"""
                ffmpeg -i "{fname}" -vf "select=eq(pict_type\,I)" -vsync vfr "{temp_dir}/frame_%05d.jpg"
                """
                with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                    process.wait()
                frames = []
                for filename in os.listdir(temp_dir):
                    if filename.endswith((".jpg")):
                        image_path = os.path.join(temp_dir, filename)
                        with Image.open(image_path) as img:
                            frames.append(img.copy())
                return frames

        def predict(self, images, labels):
            """
            Runs inference and gets label probabilities using a pre-trained CLIP-ViT-B-32.

            Args:
                images (list): List of PIL Images
                labels (list): List of labels

            Returns:
                torch.Tensor: Probability distribution across labels
            """
            inputs = processor(text=labels, images=images, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}  # move to device
            with torch.no_grad():
                output = self.model(**inputs)
                logits_per_image = output.logits_per_image
                probs = logits_per_image.softmax(dim=1)
                return probs.mean(dim=0)

        def getPredictedLabel(self):
            """
            Returns the predicted label.

            Args:
                probs (torch.Tensor): Probability distribution across labels
                labels (list): List of labels

            Returns:
                str: Predicted label
            """
            max_prob_index = self.probs.argmax().item()
            return self.labels[max_prob_index]

def run(file, labels):
    """
    Runs the operator.

    Args:
        file (dict): `VideoFactory` file object

    Returns:
        dict: A dictionary containing prediction and probabilities
    """
    fname = file["path"]
    vid_analyzer = VideoClassifier(fname, labels)
    return gendata(vid_analyzer)

def cleanup(param):
    pass

def state():
    pass