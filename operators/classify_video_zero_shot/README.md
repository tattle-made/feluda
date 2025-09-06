# Classify Video Zero Shot Operator

## Description

The `Classify Video Zero Shot` operator classifies a video into user-provided labels using the CLIP ViT-B/32 model in a zero-shot fashion. It extracts I-frames from the video using FFmpeg, then uses the CLIP model to predict the most likely label for the video content.

## Model Information

- **Model**: [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32)
- **Source**: OpenAI, via HuggingFace Transformers
- **Usage**: Zero-shot classification of video content by comparing extracted frame features to text label embeddings.

## System Dependencies

- FFmpeg
  - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH, or use `winget install ffmpeg` from an elevated PowerShell.
  - On Linux/macOS: Install via your package manager (e.g., `sudo apt install ffmpeg`).

## Operator Dependencies

- feluda[video]
- torch >= 2.6.0
- transformers >= 4.51.1
- pillow >= 11.1.0

## How to Run the Tests

1. Ensure you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/classify_video_zero_shot"
   uv pip install "feluda[dev]"
   ```

3. Ensure FFmpeg is installed and available in your PATH.
4. Run the tests:

   ```bash
   pytest operators/classify_video_zero_shot/test.py
   ```

## Usage Example

```python
from feluda.factory import VideoFactory
from operators.classify_video_zero_shot import ClassifyVideoZeroShot

# Initialize the operator
operator = ClassifyVideoZeroShot()

# Load a video
video_url = (
   "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
   )
file = VideoFactory.make_from_url(video_url)

# Classify the video
labels = ["cat", "dog"]
result = operator.run(video, labels)
print(result)
```

Output

```json
{"prediction": "cat", "probs": [0.9849101901054382, 0.015089876018464565]}
```
