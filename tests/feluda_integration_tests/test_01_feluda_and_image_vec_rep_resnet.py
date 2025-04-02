import contextlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import yaml
from requests.exceptions import ConnectTimeout

from feluda import Feluda
from feluda.models.media_factory import ImageFactory


class TestFeludaImageVectorIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""
        cls.config = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "image vectors",
                        "type": "image_vec_rep_resnet",
                        "parameters": {"index_name": "image"},
                    }
                ],
            }
        }

        # Create temporary config file using with statement to ensure proper resource cleanup
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        # Initialize Feluda
        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()

        cls.test_image_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        cls.expected_vector_dim = 512

    def setUp(self):
        """Set up test-specific feluda resources."""
        # Get operator reference in each test to ensure isolation
        self.operator = self.feluda.operators.get()["image_vec_rep_resnet"]

    def test_image_vector_generation(self):
        """Test that image vector generation works end-to-end."""
        image_obj = ImageFactory.make_from_url(self.test_image_url)
        self.assertIsNotNone(image_obj, "Image object should be successfully created")

        image_vec = self.operator.run(image_obj)

        self.assertTrue(
            isinstance(image_vec, (list, np.ndarray)),
            "Vector should be a list or numpy array",
        )
        self.assertTrue(len(image_vec) > 0, "Vector should not be empty")
        self.assertEqual(
            len(image_vec),
            self.expected_vector_dim,
            f"Vector should have dimension {self.expected_vector_dim}",
        )

        if isinstance(image_vec, np.ndarray):
            self.assertFalse(np.all(image_vec == 0), "Vector should not be all zeros")
            self.assertFalse(
                np.any(np.isnan(image_vec)), "Vector should not contain NaN values"
            )

    def test_invalid_image_url(self):
        """Test handling of invalid image URL."""
        invalid_url = "https://nonexistent-url/image.jpg"

        for exception in [ConnectTimeout]:
            with self.subTest(exception=exception.__name__):
                with patch("requests.get") as mock_get:
                    mock_get.side_effect = exception
                    result = ImageFactory.make_from_url(invalid_url)
                    self.assertIsNone(result)

    def test_operator_configuration(self):
        """Test that operator is properly configured."""
        self.assertIsNotNone(self.operator, "Operator should be properly initialized")
        self.assertTrue(
            hasattr(self.operator, "run"), "Operator should have 'run' method"
        )

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        """Context manager to verify no exception is raised."""
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Exception was raised'}: {e}")

    def test_image_vector_consistency(self):
        """Test that generating vectors twice from the same image gives consistent results."""
        image_obj = ImageFactory.make_from_url(self.test_image_url)

        with self.assertNoException(
            "First vector generation should not raise exceptions"
        ):
            vec1 = self.operator.run(image_obj)

        with self.assertNoException(
            "Second vector generation should not raise exceptions"
        ):
            vec2 = self.operator.run(image_obj)

        np.testing.assert_array_equal(
            vec1, vec2, "Vectors should be identical for the same image"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests are done."""
        try:
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
