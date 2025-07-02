# VidVecRepClip Operator

## Description

The `VidVecRepClip` operator extracts vector representations from videos using the CLIP-ViT-B-32 model. It works by extracting I-frames (keyframes) from a video file using FFmpeg, then generating a 512-dimensional feature vector for each frame using the CLIP model. The operator yields both the average vector for the video and vectors for each I-frame.

## Model Information

- **Model**: [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32)
- **Source**: OpenAI, via HuggingFace Transformers
- **Vector Size**: 512
- **Usage**: The model is used to generate embeddings for video frames, enabling downstream tasks such as video similarity, clustering, and zero-shot classification.

## System Dependencies

- Python >= 3.10
- FFmpeg
  - On Windows, you have two methods -
      1. Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
      2. Use `winget install ffmpeg` from an elevated powershell. (Make sure you have winget installed first)
  - On Linux/macOS, install via your package manager (e.g., `sudo apt install ffmpeg`).

## Operator Dependencies

- PyTorch >= 2.6.0
- Torchvision >= 0.21.0
- Transformers >= 4.51.1
- Pillow >= 11.1.0

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/vid_vec_rep_clip"
   uv pip install "feluda[dev]"
   ```

3. Ensure FFmpeg is installed and available in your PATH.
4. Run the tests:

   ```bash
   pytest operators/vid_vec_rep_clip/test.py
   ```

5. For local video tests, place a sample video at the specified path or update the test accordingly.
