import base64
import gc
import io
import os
import platform
import shutil
import stat
import struct
import subprocess
import tempfile

import wget

from feluda import Operator


class VideoHashTmk(Operator):
    """Operator to hash video files using the TMK+PDQF binary."""

    def __init__(self) -> None:
        """Initialize the VideoHashTmk operator."""
        self.tmk_binary_path = None
        self.ffmpeg_path = shutil.which("ffmpeg")
        self.setup_binary()
        self.validate_system()
        self.hash = None

    def setup_binary(self) -> None:
        """Download and setup the TMK binary."""
        TMK_BINARY_URL = "https://github.com/tattle-made/feluda/releases/download/third-party-models/tmk-hash-video"
        tmp_dir = tempfile.gettempdir()

        binary_name = (
            "tmk-hash-video.exe" if platform.system() == "Windows" else "tmk-hash-video"
        )
        self.tmk_binary_path = os.path.join(tmp_dir, binary_name)

        if not os.path.exists(self.tmk_binary_path):
            try:
                print(f"Downloading TMK binary to {self.tmk_binary_path}")
                wget.download(TMK_BINARY_URL, out=self.tmk_binary_path)
                if platform.system() != "Windows":
                    os.chmod(self.tmk_binary_path, stat.S_IRWXU)
            except Exception as e:
                raise RuntimeError(f"Failed to download TMK binary: {e}") from e

    @staticmethod
    def validate_system() -> None:
        """Validate that required system dependencies are available."""
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "FFmpeg is not installed or not found in system PATH. "
                "Please install FFmpeg to use this operator."
            )

    @staticmethod
    def extract_pure_average_feature(tmk_data: bytes) -> list[float]:
        """Extract the pure average feature from TMK binary data."""
        handle = io.BytesIO(tmk_data)

        try:
            project_magic = handle.read(4).decode("ascii")
            file_type_magic = handle.read(4).decode("ascii")
            _frame_feature_algorithm_magic = handle.read(4).decode("ascii")

            if project_magic != "TMK1":
                raise ValueError(
                    f"Invalid project magic: {project_magic}, expected TMK1"
                )
            if file_type_magic != "FVEC":
                raise ValueError(
                    f"Invalid file type magic: {file_type_magic}, expected FVEC"
                )

            num_periods = struct.unpack("i", handle.read(4))[0]
            num_fourier_coefficients = struct.unpack("i", handle.read(4))[0]
            frame_feature_dimension = struct.unpack("i", handle.read(4))[0]

            # Skip periods and fourier coefficients arrays
            handle.read(4 * num_periods)
            handle.read(4 * num_fourier_coefficients)

            # Read the pure average feature
            pure_average_feature = struct.unpack(
                "f" * frame_feature_dimension, handle.read(4 * frame_feature_dimension)
            )

            return list(pure_average_feature)
        except (struct.error, UnicodeDecodeError) as e:
            raise ValueError(f"Invalid TMK data format: {e}") from e

    def hash_video(self, video_path: str) -> str:
        """Hash a video file using TMK and return the pure average feature."""
        with tempfile.NamedTemporaryFile(suffix=".tmk", delete=False) as temp_hash_file:
            temp_hash_path = temp_hash_file.name

        try:
            cmd = [
                self.tmk_binary_path,
                "-f",
                self.ffmpeg_path,
                "-i",
                video_path,
                "-o",
                temp_hash_path,
                "-v",
            ]

            subprocess.run(cmd, capture_output=True, text=True, check=True)

            with open(temp_hash_path, "rb") as f:
                tmk_data = f.read()
                pure_average_feature = self.extract_pure_average_feature(tmk_data)
                feature_bytes = struct.pack(
                    "f" * len(pure_average_feature), *pure_average_feature
                )
                base64_hash = base64.b64encode(feature_bytes).decode("utf-8")

            self.hash = base64_hash

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"TMK binary failed to process video {video_path}: {e.stderr}"
            )
        except (struct.error, ValueError) as e:
            raise ValueError(f"Error parsing TMK file for {video_path}: {e}") from e
        finally:
            if os.path.exists(temp_hash_path):
                os.remove(temp_hash_path)

    def run(self, video_path: str) -> str:
        """Generate a perceptual hash for the given video file."""
        if not isinstance(video_path, str):
            raise ValueError("video_path must be a string")

        if not video_path.strip():
            raise ValueError("video_path cannot be empty")

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.hash_video(video_path)

        return self.hash

    def cleanup(self) -> None:
        """Clean up any resources used by the operator."""
        gc.collect()

    def state(self) -> dict:
        """Return the internal state of the operator."""
        return {
            "tmk_binary_path": self.tmk_binary_path,
            "ffmpeg_path": self.ffmpeg_path,
            "hash": self.hash,
        }
