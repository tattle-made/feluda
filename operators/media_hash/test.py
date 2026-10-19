import pytest

from feluda.factory import AudioFactory, ImageFactory, VideoFactory

from .media_hash import MediaHash

SAMPLE_IMAGE_URL = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/hindi-text-2.png"
SAMPLE_VIDEO_URL = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
SAMPLE_AUDIO_URL = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/hi_speech.wav"


@pytest.fixture(scope="module")
def operator():
    return MediaHash()


@pytest.fixture(scope="module")
def sample_image():
    return ImageFactory.make_from_url_to_path(SAMPLE_IMAGE_URL)


@pytest.fixture(scope="module")
def sample_video():
    return VideoFactory.make_from_url(SAMPLE_VIDEO_URL)


@pytest.fixture(scope="module")
def sample_audio():
    return AudioFactory.make_from_url(SAMPLE_AUDIO_URL)


def test_initialization(operator):
    assert operator is not None
    assert operator.hash is None


# --- image ---


def test_image_returns_hex_string(operator, sample_image):
    result = operator.run(sample_image)
    assert isinstance(result, str)
    assert len(result) == 128  # blake2b default: 64-byte digest = 128 hex chars
    assert all(c in "0123456789abcdef" for c in result)


def test_image_is_deterministic(operator, sample_image):
    assert operator.run(sample_image) == operator.run(sample_image)


# --- video ---


def test_video_returns_hex_string(operator, sample_video):
    result = operator.run(sample_video)
    assert isinstance(result, str)
    assert len(result) == 128
    assert all(c in "0123456789abcdef" for c in result)


def test_video_is_deterministic(operator, sample_video):
    assert operator.run(sample_video) == operator.run(sample_video)


def test_video_hash_differs_from_image(operator, sample_image, sample_video):
    assert operator.run(sample_image) != operator.run(sample_video)


# --- audio ---


def test_audio_returns_hex_string(operator, sample_audio):
    result = operator.run(sample_audio)
    assert isinstance(result, str)
    assert len(result) == 128
    assert all(c in "0123456789abcdef" for c in result)


def test_audio_is_deterministic(operator, sample_audio):
    assert operator.run(sample_audio) == operator.run(sample_audio)


def test_audio_hash_differs_from_video(operator, sample_audio, sample_video):
    assert operator.run(sample_audio) != operator.run(sample_video)


# --- error handling ---


def test_run_invalid_input(operator):
    with pytest.raises(ValueError, match="'path' key"):
        operator.run("not_a_dict")


def test_run_file_not_found(operator):
    with pytest.raises(FileNotFoundError):
        operator.run({"path": "/nonexistent/file.png"})


# --- lifecycle ---


def test_state_after_run(operator, sample_image):
    operator.run(sample_image)
    state = operator.state()
    assert "hash" in state
    assert state["hash"] is not None


def test_cleanup(operator):
    operator.cleanup()
    assert operator.state()["hash"] is None
