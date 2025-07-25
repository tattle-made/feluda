from feluda import Operator


class VideoHasher(Operator):
    """Operator to hash video files using the TMK+PDQF binary."""


def initialise(param=None):
    """
    Initializes the TMK binary. Downloads it to a temp directory if not present,
    makes it executable, and defines the hash_video function.
    :return: A callable hash_video function.
    """
    global hash_video
    global os

    import base64
    import io
    import os
    import stat
    import struct
    import subprocess
    import tempfile

    import wget

    TMK_BINARY_URL = "https://github.com/tattle-made/feluda/releases/download/third-party-models/tmk-hash-video"
    FFMPEG_PATH = r"/usr/bin/ffmpeg"
    tmp_dir = tempfile.gettempdir()
    tmk_binary_path = os.path.join(tmp_dir, "tmk-hash-video")

    if not os.path.exists(tmk_binary_path):
        print(f"Downloading TMK binary to {tmk_binary_path}")
        wget.download(TMK_BINARY_URL, out=tmk_binary_path)
        os.chmod(tmk_binary_path, stat.S_IRWXU)

    def extract_pure_average_feature(tmk_data: bytes) -> list:
        handle = io.BytesIO(tmk_data)

        project_magic = handle.read(4).decode("ascii")
        file_type_magic = handle.read(4).decode("ascii")
        _frame_feature_algorithm_magic = handle.read(4).decode("ascii")

        if project_magic != "TMK1":
            raise ValueError(f"Invalid project magic: {project_magic}, expected TMK1")
        if file_type_magic != "FVEC":
            raise ValueError(
                f"Invalid file type magic: {file_type_magic}, expected FVEC"
            )

        _frames_per_second = struct.unpack("i", handle.read(4))[0]
        num_periods = struct.unpack("i", handle.read(4))[0]
        num_fourier_coefficients = struct.unpack("i", handle.read(4))[0]
        frame_feature_dimension = struct.unpack("i", handle.read(4))[0]
        _frame_feature_count = struct.unpack("i", handle.read(4))[0]

        # Skip periods and fourier coefficients arrays
        handle.read(4 * num_periods)  # Skip periods
        handle.read(4 * num_fourier_coefficients)  # Skip fourier coefficients

        # Now read the pure average feature
        pure_average_feature = struct.unpack(
            "f" * frame_feature_dimension, handle.read(4 * frame_feature_dimension)
        )

        return list(pure_average_feature)

    def hash_video(video_path: str) -> str:
        """
        Hash a video file using TMK and return just the pure average feature as a Base64-encoded string.

        :param video_path: Path to the video file.
        :return: The pure average feature hash as a Base64-encoded string.
        """
        with tempfile.NamedTemporaryFile(suffix=".tmk", delete=False) as temp_hash_file:
            temp_hash_path = temp_hash_file.name

        try:
            subprocess.run(
                [
                    tmk_binary_path,
                    "-f",
                    FFMPEG_PATH,
                    "-i",
                    video_path,
                    "-o",
                    temp_hash_path,
                    "-v",
                ],
                check=True,
            )

            # Read the TMK file and extract pure average feature
            with open(temp_hash_path, "rb") as f:
                tmk_data = f.read()
                pure_average_feature = extract_pure_average_feature(tmk_data)

                feature_bytes = struct.pack(
                    "f" * len(pure_average_feature), *pure_average_feature
                )
                base64_hash = base64.b64encode(feature_bytes).decode("utf-8")

            return base64_hash

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error generating hash for {video_path}: {e}")
        except (struct.error, ValueError) as e:
            raise RuntimeError(f"Error parsing TMK file for {video_path}: {e}")
        finally:
            if os.path.exists(temp_hash_path):
                os.remove(temp_hash_path)

    return hash_video


def run(video_path: str) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        return hash_video(video_path)
    except Exception as e:
        print(f"An error occurred while hashing the video: {e}")
        raise e
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
