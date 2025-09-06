from unittest.mock import patch

import numpy as np
import pytest
from image_vec_rep import ImageVecRep
from requests.exceptions import ConnectTimeout

from feluda.factory import ImageFactory


@pytest.fixture(scope="session")
def image_operator():
    """Fixture to provide image vector representation operator."""
    return ImageVecRep()


@pytest.fixture(scope="session")
def test_image_url():
    """Fixture to provide test image URL."""
    return "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"


@pytest.fixture(scope="session")
def expected_vector_dim():
    """Fixture to provide expected vector dimension."""
    return 512


class TestImageVectorIntegration:
    """Test image vector representation functionality."""

    def test_image_vector_generation(
        self, image_operator, test_image_url, expected_vector_dim
    ):
        """Test that image vector generation works end-to-end."""
        image_obj = ImageFactory.make_from_url(test_image_url)
        assert image_obj is not None, "Image object should be successfully created"

        image_vec = image_operator.run(image_obj)

        assert isinstance(image_vec, (list, np.ndarray)), (
            "Vector should be a list or numpy array"
        )
        assert len(image_vec) > 0, "Vector should not be empty"
        assert len(image_vec) == expected_vector_dim, (
            f"Vector should have dimension {expected_vector_dim}"
        )

        if isinstance(image_vec, np.ndarray):
            assert not np.all(image_vec == 0), "Vector should not be all zeros"
            assert not np.any(np.isnan(image_vec)), (
                "Vector should not contain NaN values"
            )

    def test_invalid_image_url(self):
        """Test handling of invalid image URL."""
        invalid_url = "https://nonexistent-url/image.jpg"

        for exception in [ConnectTimeout]:
            with patch("requests.get") as mock_get:
                mock_get.side_effect = exception
                with pytest.raises(Exception, match="Request has timed out"):
                    ImageFactory.make_from_url(invalid_url)

    def test_operator_configuration(self, image_operator):
        """Test that operator is properly configured."""
        assert image_operator is not None, "Operator should be properly initialized"
        assert hasattr(image_operator, "run"), "Operator should have 'run' method"

    def test_image_vector_consistency(self, image_operator, test_image_url):
        """Test that generating vectors twice from the same image gives consistent results."""
        image_obj = ImageFactory.make_from_url(test_image_url)

        vec1 = image_operator.run(image_obj)
        vec2 = image_operator.run(image_obj)

        np.testing.assert_array_equal(
            vec1, vec2, "Vectors should be identical for the same image"
        )


@pytest.fixture(scope="session", autouse=True)
def cleanup_operators(image_operator):
    """Cleanup operators after each test."""
    yield
    image_operator.cleanup()
