# VideoHash Operator

## Description

The `VideoHash` operator generates perceptual hashes from video files using the TMK (Temporal Media Key) algorithm. It extracts the pure average feature from videos and returns it as a Base64-encoded string. This operator is useful for video similarity detection, duplicate detection, and content fingerprinting.

## Model Information

- **Algorithm**: TMK (Temporal Media Key) + PDQF (Perceptual Diff Quality Function)
- **Source**: [Facebook AI Research](https://github.com/facebook/ThreatExchange/tree/main/tmk)
- **Hash Type**: Pure average feature vector
- **Output Format**: Base64-encoded string
- **Usage**: The operator processes video files to generate perceptual hashes that can be used for video similarity comparison, duplicate detection, and content fingerprinting.

## Dependencies

- FFmpeg
  - On Windows, you have two methods:
      1. Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
      2. Use `winget install ffmpeg` from an elevated PowerShell (Make sure you have winget installed first)
  - On Linux/macOS, install via your package manager (e.g., `sudo apt install ffmpeg`)

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/video_hash"
   uv pip install "feluda[dev]"
   ```

3. Ensure FFmpeg is installed and available in your PATH.
4. Run the tests:

   ```bash
   pytest operators/video_hash/test.py
   ```

## Usage

### Using the Class-based Operator (Recommended)

```python
from feluda.factory import VideoFactory
from operators.video_hash import VideoHash

# Initialize the operator
operator = VideoHash()

url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"

# Load a video
video = VideoFactory.make_from_url(url)
video_path = video["path"]

# Generate hash
hash_value = operator.run(video_path)
print(f"Hash: {hash_value}")
```
