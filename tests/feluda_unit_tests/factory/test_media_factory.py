import os
import tempfile

import numpy as np
import pytest
from PIL import Image

from feluda.factory import AudioFactory, ImageFactory, VideoFactory

expected_files = [
    "text-in-image-test-hindi.png",
    "sample-cat-video.mp4.mp4",
    "audio.wav.wav",
]


@pytest.fixture(scope="module", autouse=True)
def cleanup_temp_files():
    # Setup before any tests run
    yield
    # Teardown after all tests in the module
    temp_dir = tempfile.gettempdir()
    for filename in expected_files:
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up: {file_path}")
        except Exception as e:
            print(f"Error cleaning up {file_path}: {e}")


def test_image_make_from_url():
    result = ImageFactory.make_from_url_to_path(
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
    )
    assert result["path"] is not None
    assert os.path.exists(result["path"])


@pytest.mark.skip(reason="Requires local file on disk")
def test_image_make_from_file_on_disk():
    image_path = r"core/operators/sample_data/text.png"
    image_obj = ImageFactory.make_from_file_on_disk(image_path)
    assert image_obj["image"] is not None
    assert isinstance(image_obj["image"], Image.Image)
    assert isinstance(image_obj["image_array"], np.ndarray)


def test_video_make_from_url():
    video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
    result = VideoFactory.make_from_url(video_url)
    assert result["path"] is not None
    assert os.path.exists(result["path"])


@pytest.mark.skip(reason="Requires local file on disk")
def test_video_make_from_file_on_disk():
    video_path = r"core/operators/sample_data/sample-cat-video.mp4"
    result = VideoFactory.make_from_file_on_disk(video_path)
    assert result["path"] is not None
    assert result["path"] == video_path


def test_audio_make_from_url():
    result = AudioFactory.make_from_url(
        "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/audio.wav"
    )
    assert result["path"] is not None
    assert os.path.exists(result["path"])


@pytest.mark.skip(reason="Requires local file on disk")
def test_audio_make_from_file_on_disk():
    audio_path = r"core/operators/sample_data/audio.wav"
    result = AudioFactory.make_from_file_on_disk(audio_path)
    assert result["path"] is not None
    assert result["path"] == audio_path
