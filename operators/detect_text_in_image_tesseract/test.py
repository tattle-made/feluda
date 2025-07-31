import re

import pytest

from feluda.factory import ImageFactory
from operators.detect_text_in_image_tesseract import ImageTextDetector


@pytest.fixture(scope="module")
def operator():
    operator = ImageTextDetector()
    return operator


def test_sample_image_from_url_hindi(operator: ImageTextDetector):
    image_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/hindi-text-2.png"
    image_obj = ImageFactory.make_from_url_to_path(image_url)
    image_text = operator.run(image_obj)
    expected_text = "( मेरे पीछे कौन आ रहा है)"
    assert image_text.strip() == expected_text.strip()


def test_sample_image_from_url_tamil(operator: ImageTextDetector):
    image_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/tamil-text.png"
    image_obj = ImageFactory.make_from_url_to_path(image_url)
    image_text = operator.run(image_obj)
    cleaned_image_text = re.sub(r"[\u200c\u200b]", "", image_text)
    expected_text = "காதல் மற்றும் போர்"
    assert cleaned_image_text.strip() == expected_text.strip()


def test_sample_image_from_url_telugu(operator: ImageTextDetector):
    image_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/telugu-text.png"
    image_obj = ImageFactory.make_from_url_to_path(image_url)
    image_text = operator.run(image_obj)
    expected_text = "నేను భూమిని ప్రేమిస్తున్నాను"
    assert image_text.strip() == expected_text.strip()


def test_run_invalid_file_object(operator: ImageTextDetector):
    with pytest.raises(ValueError, match="Invalid file object"):
        operator.run("not_a_dict")


def test_run_file_not_found(operator: ImageTextDetector):
    with pytest.raises(FileNotFoundError):
        operator.run({"path": "fake.png"})


def test_initialization_tesseract_not_found(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(RuntimeError, match="Tesseract OCR is not installed"):
        ImageTextDetector()


def test_cleanup_method(operator: ImageTextDetector):
    """Test that cleanup method works without errors."""
    # Should not raise any exceptions
    operator.cleanup()


def test_state_method(operator: ImageTextDetector):
    """Test that state method returns expected configuration."""
    state = operator.state()
    assert "psm" in state
    assert "oem" in state
    assert state["psm"] == 6
    assert state["oem"] == 1
