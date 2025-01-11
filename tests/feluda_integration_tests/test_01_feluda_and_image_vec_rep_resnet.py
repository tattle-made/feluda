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

        # Create temporary config file
        cls.temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        )
        yaml.dump(cls.config, cls.temp_file)
        cls.temp_file.close()

        # Initialize Feluda
        cls.feluda = Feluda(cls.temp_file.name)
        cls.feluda.setup()

    def test_image_vector_generation(self):
        """Test that image vector generation works end-to-end."""

        test_image_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        image_obj = ImageFactory.make_from_url(test_image_url)
        operator = self.feluda.operators.get()["image_vec_rep_resnet"]
        image_vec = operator.run(image_obj)

        # Basic validation
        self.assertTrue(
            isinstance(image_vec, (list, np.ndarray)),
            "Vector should be a list or numpy array",
        )
        self.assertTrue(len(image_vec) > 0, "Vector should not be empty")

        expected_dim = 512
        self.assertEqual(
            len(image_vec), expected_dim, f"Vector should have dimension {expected_dim}"
        )

        if isinstance(image_vec, np.ndarray):
            self.assertFalse(np.all(image_vec == 0), "Vector should not be all zeros")

    def test_invalid_image_url(self):
        """Test handling of invalid image URL."""
        invalid_url = "https://nonexistent-url/image.jpg"

        with patch("requests.get") as mock_get:
            mock_get.side_effect = ConnectTimeout
            result = ImageFactory.make_from_url(invalid_url)
            self.assertIsNone(result)

    def test_operator_configuration(self):
        """Test that operator is properly configured."""
        operator = self.feluda.operators.get()["image_vec_rep_resnet"]

        self.assertIsNotNone(operator, "Operator should be properly initialized")
        self.assertTrue(hasattr(operator, "run"), "Operator should have 'run' method")

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests are done."""
        Path(cls.temp_file.name).unlink()
