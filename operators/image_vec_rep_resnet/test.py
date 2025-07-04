import io

import numpy as np
import pytest
from PIL import Image

from feluda.factory import ImageFactory
from operators.image_vec_rep_resnet import ImageVecRepResnet


@pytest.fixture
def operator():
    """Fixture to create and cleanup ImageVecRepResnet instance."""
    operator = ImageVecRepResnet()
    yield operator
    operator.cleanup()


@pytest.fixture
def sample_image():
    """Fixture to create a sample PIL Image for testing."""
    return Image.new("RGB", (224, 224), color="red")


@pytest.fixture
def sample_image_obj(sample_image):
    """Fixture to create a sample image object from ImageFactory."""
    buffer = io.BytesIO()
    sample_image.save(buffer, format="PNG")
    buffer.seek(0)
    image_obj = ImageFactory.make_from_file_in_memory(buffer)
    return image_obj


class TestImageVecRepResnet:
    """Test suite for ImageVecRepResnet operator."""

    def test_initialization(self):
        """Test that the operator initializes correctly."""
        operator = ImageVecRepResnet()
        assert operator.model is not None
        assert operator.feature_layer is not None
        assert operator.transform is not None
        assert operator.image is None
        operator.cleanup()

    def test_extract_feature_valid_input(self, operator, sample_image):
        """Test feature extraction with valid PIL Image input."""
        result = operator.extract_feature(sample_image)

        assert isinstance(result, np.ndarray)
        assert result.shape == (512,)
        assert result.dtype == np.float16

    def test_extract_feature_invalid_input_type(self, operator):
        """Test that extract_feature raises ValueError for invalid input types."""
        invalid_inputs = [
            "not an image",
            123,
            None,
            {"image": "fake"},
            np.zeros((224, 224, 3)),
        ]

        for invalid_input in invalid_inputs:
            with pytest.raises(TypeError, match="must be a PIL.Image.Image object"):
                operator.extract_feature(invalid_input)

    def test_run_valid_input(self, operator, sample_image_obj):
        """Test run method with valid ImageFactory output."""
        result = operator.run(sample_image_obj)

        assert isinstance(result, np.ndarray)
        assert result.shape == (512,)
        assert result.dtype == np.float16

    @pytest.mark.parametrize(
        "invalid_input",
        ["not a dict", {"not_image": 123}, {}, None],
    )
    def test_run_invalid_input_value_error(self, operator, invalid_input):
        with pytest.raises(ValueError, match="must be a dict with an 'image' key"):
            operator.run(invalid_input)

    def test_run_invalid_image_type(self, operator):
        """Test run method when 'image' value is not a PIL Image."""
        invalid_obj = {"image": "not a PIL image"}
        with pytest.raises(TypeError):
            operator.run(invalid_obj)

    def test_run_missing_image_key(self, operator):
        """Test run method when 'image' key is missing from input dict."""
        invalid_obj = {"image_array": np.zeros((224, 224, 3))}
        with pytest.raises(ValueError, match="must be a dict with an 'image' key"):
            operator.run(invalid_obj)

    def test_image_conversion_to_rgb(self, operator):
        """Test that images are converted to RGB format."""
        # Create a grayscale image
        gray_image = Image.new("L", (224, 224), color=128)
        image_obj = {"image": gray_image}

        result = operator.run(image_obj)
        assert isinstance(result, np.ndarray)
        assert result.shape == (512,)

    def test_with_real_image_from_url(self, operator):
        """Integration test with real image from URL."""
        try:
            image_obj = ImageFactory.make_from_url(
                "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
            )
            result = operator.run(image_obj)

            assert isinstance(result, np.ndarray)
            assert result.shape == (512,)
            assert result.dtype == np.float16
        except Exception as e:
            pytest.skip(f"Network test failed: {e}")

    @pytest.mark.parametrize("image_size", [(100, 100), (500, 500), (224, 224)])
    def test_different_image_sizes(self, operator, image_size):
        """Test that the operator works with different image sizes."""
        test_image = Image.new("RGB", image_size, color="blue")
        image_obj = {"image": test_image}

        result = operator.run(image_obj)
        assert isinstance(result, np.ndarray)
        assert result.shape == (512,)
