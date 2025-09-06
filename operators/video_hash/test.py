import base64
import os

import pytest

from feluda.factory import VideoFactory

from .video_hash import VideoHash


@pytest.fixture(scope="module")
def operator():
    """Create a VideoHash operator instance for testing."""
    return VideoHash()


@pytest.fixture
def sample_video_url():
    """Sample video URL for testing."""
    return "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"


def test_operator_initialization(operator):
    """Test that the operator initializes correctly."""
    assert operator is not None
    assert operator.tmk_binary_path is not None
    assert operator.ffmpeg_path is not None
    assert os.path.exists(operator.tmk_binary_path)


def test_video_hashing_from_url(operator, sample_video_url):
    video_obj = VideoFactory.make_from_url(sample_video_url)
    video_path = video_obj["path"]

    # Ensure the video file exists and is accessible
    assert os.path.exists(video_path), f"Video file not found at {video_path}"
    assert os.path.isfile(video_path), f"Path is not a file: {video_path}"
    assert os.path.getsize(video_path) > 0, f"Video file is empty: {video_path}"

    hash_value = operator.run(video_path)

    assert hash_value is not None, "Hash value should not be None"
    assert isinstance(hash_value, str), (
        f"Hash should be a string, got {type(hash_value)}"
    )
    assert len(hash_value) > 0, "Hash should not be empty"

    try:
        decoded_bytes = base64.b64decode(hash_value)
        assert len(decoded_bytes) > 0, "Decoded hash should not be empty"
        assert len(decoded_bytes) % 4 == 0, (
            "Hash should be divisible by 4 bytes (float size)"
        )
    except Exception as e:
        pytest.fail(f"Hash is not valid Base64: {e}")

    expected_hash_chars = "AnMnw7sQqEOw7CxD+7J5wk1V/sKQy6NDTq2gwv4GBsMkrRxCOd78vpnrEELX8n3C+DmZwa5HtUE2lTtBa41VQaJfm8NU+vlBSeWdQhtjesG1LjLDUOjNQqaSKkI4DM3C4XUBQgxv5kEZsBpCnKSewvFSL8Fki0LB+zxvwFQLVkGgIQrCqUEkQwFF80KPJrLCGm7cwY/8u0GynXpCfEztwb9vfcFrYBtBlSC2QB7WJ0G+ginBusmEwQ5UV8F6oL/BKHk+Q4680ELo/j7DDlXwQg3gsEIS20TCsdIBwux0E0JhytLBsmRfwtNnnMHYcrK/04cmQuZEysHCNfbAvZyKQYQCs8Fa2eHCyPp5Qjeli0I2hQrD4d8KwtaWoECMQK3AIHCqQRs4VsJW6BpBk1GoQWD6AsFQuqdAyxRoQXE7AsLHPgDCEjYMQoUgeEI6FZLCHPUAwqRtUUEL5aM/l6A9QpQmskHdSqtB7u6IwR7C9T+axzC/ywKTwXwCkEC+6e7AbvwAQn3wSkKne5XAbAeNwW1vE0Kr8YNCTYgKwWchwr/c4/TBEsmvwf5RtcBQjwbBtKJoQZdI/cHWpmlBuXjzP3b2JMJs8gLCmh+7QbSn+cGGwce/+6NdQOcfNMLaVZvA78wFwnZOicENW5rAeo1jPzm3FEI5r91BvQE1wYOkacCTPYPCOPHpwV2kIUEEUuzBRwsbwqC5KEFNuKpBpaB0wVFhe8Hx+tlBeayoQZ5zmUCHbqPA8MxFwdSnNUECRgnBdGCPwoMNjUJiCKJBJlw5wt9PIkFHtHNBaCdVvwvxHUFtnAHBt5+fQH2ZnkG/90HAcCBawXbz0sGDigxAosZewZOXicJgYJPAjQnGQdQzp8Azq5VBD7ymwQX0KcH+x4K/cPfQQCmMM0FuABrBVYFvwWR23EAYyTfAys4SwbQDrEG68mHC7QUYwiAt+cFdpbg/dHnYQbEYsEEqpHDB9+EvwcWZyL61YmBB4V+lwArdrMCVbTxAsvFxPzDuhUC+PPxAqkMewfHAQMJ45dPAVM9+QSXqxUGFzFzBKkTCQJDF+kCZPnBAYiIkwTbumEFoN39BZUmGwVphFME4mwxAgmBkQMLPo8Cgsw7CUr5dQYhY9EGjWMFAwruiwbzZjsHRask+/yZ/QasWVEGvDUbAhJFrQBqbGcE2/j5A98vcQDYFU8ErA11A3/KpwSpoE0CVc9NBSvKdPzsE2sArIeI+GvSfwZRUY0E7ZTdBesM1QY6qSMHiyNTADVERQcrdOkEsxZnAhcOEwGRABML0yF++COXpQI14CEH9ktDA1sShQOA6H0Egy6/AlExnvw2NVUDVQzlBRcEewco7Ub8e4iJBic5UwA=="

    assert all(c in expected_hash_chars for c in hash_value), (
        f"Hash contains invalid characters: {hash_value}"
    )


def test_invalid_video_path(operator):
    """Test error handling for non-existent video file."""
    with pytest.raises(FileNotFoundError, match="Video file not found"):
        operator.run("non_existent_video.mp4")
