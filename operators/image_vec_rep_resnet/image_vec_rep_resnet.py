import gc

import numpy as np
import torch
import torchvision.models as models
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms

from feluda.factory import ImageFactory


class ImageVecRepResnet:
    """Operator to extract image vector representations using ResNet18."""

    def __init__(self) -> None:
        """
        Initializes the ImageVecRepResnet operator with a pre-trained ResNet18 model.
        """
        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        self.feature_layer = self.model._modules.get("avgpool")
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.image = None

    def extract_feature(self, img: Image.Image) -> np.ndarray:
        """
        Extracts a 512-dimensional feature vector from a PIL Image using ResNet18.

        Args:
            img (Image.Image): Input image (must be a PIL Image).

        Returns:
            np.ndarray: 512-dimensional feature vector (float16).

        """
        if not isinstance(img, Image.Image):
            raise TypeError(
                "Input to extract_feature must be a PIL.Image.Image object."
            )
        self.image = img = Variable(self.transform(img)).unsqueeze(0)
        embedding = torch.zeros(512)

        def hook(m, i, o):
            feature_data = o.data.reshape(512)
            embedding.copy_(feature_data)

        h = self.feature_layer.register_forward_hook(hook)
        self.model(img)
        h.remove()
        embedding_fp16 = np.array(embedding.numpy(), dtype=np.float16)
        return embedding_fp16

    def run(self, image_obj: ImageFactory) -> np.ndarray:
        """
        Runs the operator on an image object from ImageFactory.

        Args:
            image_obj (dict): Dictionary with key 'image' containing a PIL Image.

        Returns:
            np.ndarray: 512-dimensional feature vector.
        """
        if not isinstance(image_obj, dict) or "image" not in image_obj:
            raise ValueError(
                "Input to run() must be a dict with an 'image' key (from ImageFactory)."
            )
        image = image_obj["image"]
        if not isinstance(image, Image.Image):
            raise TypeError(
                "The 'image' value in input dict must be a PIL.Image.Image object."
            )
        image = image.convert("RGB")
        image_vec = self.extract_feature(image)
        return image_vec

    def state(self) -> dict:
        """
        Returns the current state of the operator.

        Returns:
            dict: State of the operator
        """
        return {
            "model": self.model,
            "feature_layer": self.feature_layer,
            "transform": self.transform,
            "image": self.image,
        }

    def cleanup(self) -> None:
        """
        Cleans up resources used by the operator.
        """
        del self.model
        del self.feature_layer
        del self.transform
        del self.image
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
