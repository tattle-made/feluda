def initialise(param=None):
    """
    Initializes the TMK binary. Downloads it to a temp directory if not present,
    makes it executable, and defines the hash_video function.
    :return: A callable hash_video function.
    """
    global hash_video
    global os

    import base64
    import os
    import stat
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

    def hash_video(video_path: str) -> str:
        """
        Hash a video file using the TMK+PDQF binary and return the hash as a Base64-encoded string.

        :param video_path: Path to the video file.
        :return: The hash as a Base64-encoded string.
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

            with open(temp_hash_path, "rb") as f:
                binary_data = f.read()
                base64_hash = base64.b64encode(binary_data).decode("utf-8")
            return base64_hash
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error generating hash for {video_path}: {e}")
        finally:
            if os.path.exists(temp_hash_path):
                os.remove(temp_hash_path)
                pass

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
