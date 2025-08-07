import pytest

from feluda.factory import ImageFactory

from .detect_lewd_images import LewdImageDetector


@pytest.fixture(scope="module")
def operator():
    """Create a LewdImageDetector instance for testing."""
    return LewdImageDetector()


def test_sample_image_from_url(operator: LewdImageDetector):
    """Test inference on a downloaded image from URL."""
    image_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/text.png"
    image = ImageFactory.make_from_url_to_path(image_url)
    result = operator.run(image)

    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


@pytest.mark.skip(reason="This test requires a local image file.")
def test_sample_image_from_disk(operator: LewdImageDetector):
    """Test inference on a local image file."""
    image = ImageFactory.make_from_file_on_disk_to_path(
        "operators/detect_lewd_images/image2.png"
    )
    result = operator.run(image)

    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


def test_run_invalid_file_object(operator: LewdImageDetector):
    """Test handling of invalid file object."""
    with pytest.raises(ValueError, match="Invalid file object"):
        operator.run("not_a_dict")


def test_run_missing_path(operator: LewdImageDetector):
    """Test handling of file object without path."""
    with pytest.raises(ValueError, match="Image path must not be empty"):
        operator.run({"path": ""})


def test_run_empty_path(operator: LewdImageDetector):
    """Test handling of empty path."""
    with pytest.raises(ValueError, match="Image path must not be empty"):
        operator.run({"path": ""})


def test_run_file_not_found(operator: LewdImageDetector):
    """Test handling of nonexistent file."""
    with pytest.raises(FileNotFoundError):
        operator.run({"path": "nonexistent_file.jpg"})


def test_cleanup(operator: LewdImageDetector):
    """Test cleanup method."""
    operator.cleanup()
    assert operator.model is None


def test_state(operator: LewdImageDetector):
    """Test state method."""
    state = operator.state()
    assert isinstance(state, dict)
    assert "model" in state
