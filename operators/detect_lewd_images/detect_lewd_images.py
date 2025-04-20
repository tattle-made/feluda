def initialize(param):
    """
    Initializes the operator.

    Args:
        param (dict): Parameters for initialization
    """
    print("Installing packages for classify_video_zero_shot")
    global inference
    global model
    global pad_resize_image
    global preprocess_for_evaluation
    global read_image
    global os

    import logging
    import os

    import tensorflow as tf
    from huggingface_hub import snapshot_download

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    logging.basicConfig(level=logging.ERROR)

    tf.get_logger().setLevel(logging.ERROR)
    logging.getLogger("absl").setLevel(logging.ERROR)

    # Load the model and processor
    local_dir = snapshot_download(repo_id="nateraw/bumble-private-detector")
    print("Model downloaded to:", local_dir)
    model = tf.saved_model.load(local_dir)

    def pad_resize_image(image: tf.Tensor, dims: tuple[int, int]) -> tf.Tensor:
        """
        Resize image with padding

        Parameters
        ----------
        image : tf.Tensor
            Image to resize
        dims : tuple[int, int]
            Dimensions of resized image

        Returns
        -------
        image : tf.Tensor
            Resized image
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
        image: tf.Tensor, image_size: int, dtype: tf.dtypes.DType
    ) -> tf.Tensor:
        """
        Preprocess image for evaluation

        Parameters
        ----------
        image : tf.Tensor
            Image to be preprocessed
        image_size : int
            Height/Width of image to be resized to
        dtype : tf.dtypes.DType
            Dtype of image to be used

        Returns
        -------
        image : tf.Tensor
            Image ready for evaluation
        """
        image = pad_resize_image(image, [image_size, image_size])

        image = tf.cast(image, dtype)

        image -= 128
        image /= 128

        return image

    def read_image(filename: str) -> tf.Tensor:
        """
        Load and preprocess image for inference with the Private Detector

        Parameters
        ----------
        filename : str
            Filename of image

        Returns
        -------
        image : tf.Tensor
            Image ready for inference
        """
        image = tf.io.read_file(filename)
        image = tf.io.decode_jpeg(image, channels=3)

        image = preprocess_for_evaluation(image, 480, tf.float16)

        image = tf.reshape(image, -1)

        return image

    def inference(image_path: str):
        """Get predictions with a Private Detector model

        Parameters
        ----------
        image_path : str
            Path to image to be predicted on

        Returns
        -------
        preds
            Prediction result
        """
        try:
            image = read_image(image_path)
            preds = model([image])
            probability = tf.get_static_value(preds[0])[0]
            return probability
        except Exception as e:
            print(f"[ERROR] Inference failed on '{image_path}': {e}")
            return None


def run(image_path: str):
    """
    Runs the operator.

    Args:
        image_path (str): Path to the image file

    Returns:
        Prediction results
    """
    fname = image_path["path"]
    if not fname:
        raise ValueError("Image path must not be empty.")
    try:
        result = inference(fname)
        return result
    finally:
        os.remove(fname)
