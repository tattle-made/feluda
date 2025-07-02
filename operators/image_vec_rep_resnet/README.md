# ImageVecRep-Resnet Operator

## Description

The `ImageVecRep-Resnet` operator extracts vector representations from images using the ResNet18 model. It generates a 512-dimensional feature vector from input images, enabling downstream tasks such as image similarity, clustering, and classification. The operator uses the pre-trained ResNet18 model with ImageNet weights and extracts features from the average pooling layer.

## Model Information

- **Model**: [ResNet18](https://pytorch.org/vision/stable/models.html#torchvision.models.resnet18)
- **Source**: PyTorch Vision Models
- **Vector Size**: 512
- **Usage**: The model is used to generate embeddings for images, enabling downstream tasks such as image similarity, clustering, and classification.

## System Dependencies

- Python >= 3.8

## Operator Dependencies

- PyTorch >= 1.9.0
- Torchvision >= 0.10.0
- Pillow >= 8.0.0
- NumPy >= 1.19.0

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/image_vec_rep_resnet"
   uv pip install "feluda[dev]"
   ```

3. Run the tests:

   ```bash
   pytest operators/image_vec_rep_resnet/test.py
   ```

## Usage

```python
from feluda.factory import ImageFactory
from operators.image_vec_rep_resnet.image_vec_rep_resnet import ImageVecRepResnet

# Initialize the operator
operator = ImageVecRepResnet()

# Load an image
image_obj = ImageFactory.make_from_url("https://example.com/image.jpg")

# Extract features
features = operator.run(image_obj)
print(f"Feature vector shape: {features.shape}")  # (512,)
print(f"Feature vector dtype: {features.dtype}")  # float16

# Cleanup
operator.cleanup()
```
