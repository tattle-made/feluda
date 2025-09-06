# DetectTextInImage Operator

## Description

The `DetectTextInImage` operator extracts text from images using Tesseract OCR (Optical Character Recognition). It supports multiple languages including English, Hindi, Tamil, and Telugu. The operator processes image files and returns the detected text as a string.

## Model Information

- **OCR Engine**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- **Source**: Google, via pytesseract Python wrapper
- **Supported Languages**: English (eng), Hindi (hin), Tamil (tam), Telugu (tel)
- **Usage**: The operator uses Tesseract's OCR capabilities to extract text from images, enabling downstream tasks such as text analysis, content moderation, and document processing.

## System Dependencies

- Tesseract OCR
  - On Windows:
      1. Download from [UB-Mannheim's Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
      2. Install and add to PATH
      3. Install language packs for Hindi, Tamil, and Telugu
  - On Linux: `sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-tam tesseract-ocr-tel`
  - On macOS: `brew install tesseract tesseract-lang`

## Operator Dependencies

- pytesseract >= 0.3.10
- Pillow >= 11.1.0

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/detect_text_in_image"
   uv pip install "feluda[dev]"
   ```

3. Ensure Tesseract OCR is installed and available in your PATH.
4. Run the tests:

   ```bash
   pytest operators/detect_text_in_image/test.py
   ```

## Usage

```python
from feluda.factory import ImageFactory
from operators.detect_text_in_image import DetectTextInImage

# Initialize the operator
operator = DetectTextInImage()

# Load an image
image = ImageFactory.make_from_url_to_path("https://example.com/image.png")

# Extract text
text = operator.run(image, remove_after_processing=False)
print(text)

# Check operator state
state = operator.state()
print(f"PSM: {state['psm']}, OEM: {state['oem']}")

# Cleanup resources
operator.cleanup()
```

## Configuration

The operator accepts two configuration parameters:

- **psm** (int): Page segmentation mode (default: 6)
- **oem** (int): OCR Engine mode (default: 1)

These can be set during initialization:

```python
operator = DetectTextInImage(psm=8, oem=3)
```
