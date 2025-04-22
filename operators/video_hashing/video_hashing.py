import base64
import os
import subprocess
import tempfile

# Binary path for TMK+PDQF
TMK_BINARY = os.path.join(os.path.dirname(__file__), "bin", "tmk-hash-video")
FFMPEG_PATH = "/usr/bin/ffmpeg"  # Replace with the actual path to ffmpeg in your system

def hash_video(video_path: str) -> str:
    """
    Hash a video file using the TMK+PDQF binary and return the hash as a Base64-encoded string.

    :param video_path: Path to the video file.
    :return: The hash as a Base64-encoded string.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Use a temporary file to store the hash
    with tempfile.NamedTemporaryFile(suffix=".tmk", delete=False) as temp_hash_file:
        temp_hash_path = temp_hash_file.name

    try:
        # Run the TMK binary to generate the hash
        subprocess.run(
            [
                TMK_BINARY,
                "-f", FFMPEG_PATH,
                "-i", video_path,
                "-o", temp_hash_path,
                "-v",
            ],
            check=True,
        )

        # Read the binary hash file and encode it as Base64
        with open(temp_hash_path, "rb") as f:
            binary_data = f.read()
            base64_hash = base64.b64encode(binary_data).decode("utf-8")
        return base64_hash
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error generating hash for {video_path}: {e}")
    finally:
        # delete the temporary hash file
        if os.path.exists(temp_hash_path):
            os.remove(temp_hash_path)
