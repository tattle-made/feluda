# LewdImageDetector Operator

## Description

The `LewdImageDetector` operator detects inappropriate or lewd content in images using the Bumble Private Detector model. It analyzes images and returns a probability score indicating the likelihood of inappropriate content being present. The operator is designed to help moderate content by identifying potentially problematic images.

## Model Information

- **Model**: [Bumble Private Detector](https://huggingface.co/nateraw/bumble-private-detector)
- **Source**: Bumble, via HuggingFace Hub
- **Framework**: TensorFlow
- **Input**: Images (various formats supported)
- **Output**: Probability score (0.0 to 1.0) indicating likelihood of inappropriate content
- **Usage**: The model is used for content moderation and filtering inappropriate images from datasets or applications.

## Dependencies

- TensorFlow >= 2.19.0
- HuggingFace Hub >= 0.30.2

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/detect_lewd_images"
   uv pip install "feluda[dev]"
   ```

3. Run the tests:

   ```bash
   pytest operators/detect_lewd_images/test.py
   ```

## Usage

```python
from feluda.factory import ImageFactory
from operators.detect_lewd_images import LewdImageDetector

# Initialize the operator
operator = LewdImageDetector()

# Load an image
image = ImageFactory.make_from_url_to_path("https://example.com/image.jpg")

# Detect inappropriate content
probability = operator.run(image)

print(f"Probability of inappropriate content: {probability:.3f}")

# Cleanup
operator.cleanup()
```

## Output Format

The operator returns a float value between 0.0 and 1.0:
- **0.0**: Very low probability of inappropriate content
- **1.0**: Very high probability of inappropriate content
