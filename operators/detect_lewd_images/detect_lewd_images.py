import contextlib
import gc
import logging
import os

import tensorflow as tf
from huggingface_hub import snapshot_download

from feluda import Operator
from feluda.factory import ImageFactory


class DetectLewdImages(Operator):
    """Operator to detect lewd images using the Bumble Private Detector model.

    This operator uses a pre-trained TensorFlow model to classify images
    and determine if they contain inappropriate content.
    """

    def __init__(self) -> None:
        """Initialize the DetectLewdImages class."""
        self.model = None
        self.setup_logging()
        self.load_model()

    @staticmethod
    def setup_logging() -> None:
        """Configure logging to suppress TensorFlow warnings."""
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        logging.basicConfig(level=logging.ERROR)
        tf.get_logger().setLevel(logging.ERROR)
        logging.getLogger("absl").setLevel(logging.ERROR)

    def load_model(self) -> None:
        """Load the Bumble Private Detector model from HuggingFace Hub."""
        try:
            local_dir = snapshot_download(repo_id="nateraw/bumble-private-detector")
            self.model = tf.saved_model.load(local_dir)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load the Bumble Private Detector model: {e!s}"
            ) from e

    @staticmethod
    def pad_resize_image(image: tf.Tensor, dims: tuple[int, int]) -> tf.Tensor:
        """Resize image with padding to maintain aspect ratio.

        Args:
            image: Image tensor to resize
            dims: Target dimensions (height, width)

        Returns:
            Resized and padded image tensor
        """
        image = tf.image.resize(image, dims, preserve_aspect_ratio=True)
        shape = tf.shape(image)

        sxd = dims[1] - shape[1]
        syd = dims[0] - shape[0]

        sx = tf.cast(sxd / 2, dtype=tf.int32)
        sy = tf.cast(syd / 2, dtype=tf.int32)

        paddings = tf.convert_to_tensor([[sy, syd - sy], [sx, sxd - sx], [0, 0]])
        image = tf.pad(image, paddings, mode="CONSTANT", constant_values=128)

        return image

    def preprocess_for_evaluation(
        self, image: tf.Tensor, image_size: int, dtype: tf.dtypes.DType
    ) -> tf.Tensor:
        """Preprocess image for evaluation with the Private Detector.

        Args:
            image: Image tensor to preprocess
            image_size: Target size for height/width
            dtype: Data type for the image

        Returns:
            Preprocessed image tensor ready for inference
        """
        image = self.pad_resize_image(image, [image_size, image_size])
        image = tf.cast(image, dtype)
        image -= 128
        image /= 128
        return image

    def read_image(self, filename: str) -> tf.Tensor:
        """Load and preprocess image for inference.

        Args:
            filename: Path to the image file

        Returns:
            Preprocessed image tensor
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image file not found: {filename}")

        try:
            raw = tf.io.read_file(filename)
            image = tf.io.decode_image(raw, channels=3, expand_animations=True)
            image.set_shape([None, None, 3])
            image = self.preprocess_for_evaluation(image, 480, tf.float16)
            return tf.reshape(image, -1)
        except Exception as e:
            raise ValueError(f"Failed to decode image {filename}: {e!s}") from e

    def inference(self, image_path: str) -> float:
        """Perform inference on an image using the Private Detector model.

        Args:
            image_path: Path to the image file

        Returns:
            Probability score indicating likelihood of inappropriate content
        """
        try:
            image = self.read_image(image_path)
            preds = self.model([image])
            probability = preds[0].numpy()[0]
            return float(probability)
        except (FileNotFoundError, ValueError):
            raise
        except Exception as e:
            raise RuntimeError(f"Inference failed on '{image_path}': {e!s}") from e

    def run(self, file: ImageFactory, remove_after_processing: bool = False) -> float:
        """Run the lewd image detection operator.

        Args:
            file: ImageFactory file object containing the image path
            remove_after_processing: Whether to remove the file after processing

        Returns:
            Probability score (0.0 to 1.0) indicating likelihood of inappropriate content
        """
        if not isinstance(file, dict) or "path" not in file:
            raise ValueError(
                "Invalid file object. Expected ImageFactory object with 'path' key."
            )

        fname = file["path"]
        if not fname:
            raise ValueError("Image path must not be empty.")

        try:
            result = self.inference(fname)
            return result
        finally:
            if remove_after_processing:
                with contextlib.suppress(FileNotFoundError):
                    os.remove(fname)

    def cleanup(self) -> None:
        """Clean up resources used by the operator."""
        self.model = None
        gc.collect()

    def state(self) -> dict:
        """Return the current state of the operator.

        Returns:
            Dictionary containing the operator's current state
        """
        return {"model": self.model}
