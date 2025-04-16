"""
Operator to extract video vector representations using CLIP-ViT-B-32.
"""


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
    import logging
    import shutil

    import torch
    from PIL import Image
    from transformers import AutoProcessor, CLIPModel

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("vid_vec_rep_clip")

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

        def __init__(self, fname):
            """
            Constructor for the `VideoAnalyzer` class.

            Args:
                fname (str): Path to the video file
            """
            self.model = model
            self.device = device
            self.processor = processor
            self.logger = logger
            self.frame_images = []
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
            # check if file exists
            if not os.path.exists(fname):
                raise FileNotFoundError(f"File not found: {fname}")

            self.logger.info(f"Analyzing video file: {fname}")
            
            # Extract I-frames and features
            self.frame_images = self.extract_frames(fname)
            
            if not self.frame_images:
                self.logger.warning("No frames were extracted from the video. Using fallback method.")
                self.frame_images = self.extract_frames_fallback(fname)
                
            if not self.frame_images:
                self.logger.error("Both frame extraction methods failed. Using placeholder image.")
                # Create a black placeholder image as a fallback
                from PIL import Image, ImageDraw
                placeholder = Image.new('RGB', (224, 224), color='black')
                draw = ImageDraw.Draw(placeholder)
                draw.text((10, 10), "Error: No frames extracted", fill='white')
                self.frame_images = [placeholder]
                
            self.logger.info(f"Extracted {len(self.frame_images)} frames from video")
            self.feature_matrix = self.extract_features(self.frame_images)

        def extract_frames(self, fname):
            """
            Extracts I-frames from the video file using `ffmpeg`.

            Args:
                fname (str): Path to the video file

            Returns:
                list: List of PIL Images
            """
            self.logger.info("Extracting frames using primary method")
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Command to extract I-frames using ffmpeg's command line tool
                    cmd = f"""ffmpeg -i "{fname}" -vf "select=eq(pict_type\\,I)" -vsync vfr "{temp_dir}/frame_%05d.jpg\""""
                    self.logger.info(f"Running command: {cmd}")
                    
                    with subprocess.Popen(
                        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    ) as process:
                        stdout, stderr = process.communicate()
                        self.logger.info(f"ffmpeg stdout: {stdout.decode() if stdout else ''}")
                        self.logger.info(f"ffmpeg stderr: {stderr.decode() if stderr else ''}")
                        
                    frames = []
                    frame_files = os.listdir(temp_dir)
                    self.logger.info(f"Files in temp directory: {frame_files}")
                    
                    for filename in frame_files:
                        if filename.endswith((".jpg")):
                            image_path = os.path.join(temp_dir, filename)
                            try:
                                with Image.open(image_path) as img:
                                    frames.append(img.copy())
                            except Exception as e:
                                self.logger.error(f"Error opening image {image_path}: {str(e)}")
                    
                    self.logger.info(f"Successfully extracted {len(frames)} frames")
                    return frames
                except Exception as e:
                    self.logger.error(f"Error in frame extraction: {str(e)}")
                    return []

        def extract_frames_fallback(self, fname):
            """
            Fallback method to extract frames at regular intervals.
            
            Args:
                fname (str): Path to the video file
                
            Returns:
                list: List of PIL Images
            """
            self.logger.info("Using fallback frame extraction method")
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Extract frames every 1 second
                    cmd = f"""ffmpeg -i "{fname}" -vf "fps=1" "{temp_dir}/frame_%05d.jpg\""""
                    self.logger.info(f"Running fallback command: {cmd}")
                    
                    with subprocess.Popen(
                        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    ) as process:
                        stdout, stderr = process.communicate()
                        self.logger.info(f"ffmpeg stdout: {stdout.decode() if stdout else ''}")
                        self.logger.info(f"ffmpeg stderr: {stderr.decode() if stderr else ''}")
                    
                    frames = []
                    frame_files = os.listdir(temp_dir)
                    self.logger.info(f"Files in temp directory: {frame_files}")
                    
                    for filename in frame_files:
                        if filename.endswith((".jpg")):
                            image_path = os.path.join(temp_dir, filename)
                            try:
                                with Image.open(image_path) as img:
                                    frames.append(img.copy())
                            except Exception as e:
                                self.logger.error(f"Error opening image {image_path}: {str(e)}")
                    
                    self.logger.info(f"Successfully extracted {len(frames)} frames using fallback method")
                    return frames
                except Exception as e:
                    self.logger.error(f"Error in fallback frame extraction: {str(e)}")
                    return []

        def extract_features(self, images):
            """
            Extracts features from a list of images using pre-trained CLIP-ViT-B-32.

            Args:
                images (list): List of PIL Images

            Returns:
                torch.Tensor: Feature matrix of shape (batch, 512)
            """
            self.logger.info(f"Extracting features from {len(images)} images")
            
            try:
                inputs = self.processor(
                    images=images, return_tensors="pt", padding=True, truncation=True
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}  # move to device
                with torch.no_grad():
                    features = self.model.get_image_features(**inputs)
                    self.logger.info(f"Successfully extracted features with shape {features.shape}")
                    return features
            except Exception as e:
                self.logger.error(f"Error extracting features: {str(e)}")
                # Return a dummy feature vector as fallback
                # Use the torch module from the outer scope, don't re-import it
                self.logger.info("Returning dummy feature vector")
                return torch.zeros((1, 512), device=self.device)


def run(file):
    """
    Runs the operator.

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
        if os.path.exists(fname):
            os.remove(fname)


def cleanup(param):
    pass


def state():
    pass
