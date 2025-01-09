import unittest
from pathlib import Path

import yaml

from feluda import Feluda


class TestFeludaImageVectorIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize Feluda with the existing config file."""
        cls.config_path = r"tests/feluda_integration_tests/01_config.yml"

        # Verify config file exists
        if not Path(cls.config_path).exists():
            raise unittest.SkipTest(f"Config file not found at {cls.config_path}")

        # Initialize Feluda
        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()
        print("Feluda Setup Complete")

    def test_config_loading(self):
        """Test that config is loaded correctly."""
        # Verify config file is accessible
        self.assertTrue(hasattr(self.feluda, 'config_path'),
                       "Feluda should have config_path attribute")
        self.assertEqual(self.feluda.config_path, self.config_path,
                        "Config path should match the provided path")

        # Load config directly to verify content
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Verify expected operator configuration
        operator_params = None
        for param in config['operators']['parameters']:
            if param['type'] == 'image_vec_rep_resnet':
                operator_params = param
                break

        self.assertIsNotNone(operator_params,
                            "image_vec_rep_resnet operator should be configured")

    # def test_image_vector_generation(self):
    #     """Test that image vector generation works end-to-end."""
    #     # Test with a known image URL
    #     test_image_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"

    #     # Create image object
    #     image_obj = ImageFactory.make_from_url(test_image_url)

    #     # Get the operator
    #     operator = self.feluda.operators.get()["image_vec_rep_resnet"]

    #     # Generate vector
    #     image_vec = operator.run(image_obj)

    #     # Basic validation
    #     self.assertTrue(isinstance(image_vec, (list, np.ndarray)),
    #                    "Vector should be a list or numpy array")
    #     self.assertTrue(len(image_vec) > 0,
    #                    "Vector should not be empty")

    #     expected_dim = 512
    #     self.assertEqual(len(image_vec), expected_dim,
    #                     f"Vector should have dimension {expected_dim}")

    #     if isinstance(image_vec, np.ndarray):
    #         self.assertTrue(np.all(np.isfinite(image_vec)),
    #                       "All vector values should be finite")
    #         self.assertFalse(np.all(image_vec == 0),
    #                        "Vector should not be all zeros")

    # def test_invalid_image_url(self):
    #     """Test handling of invalid image URL."""
    #     invalid_url = "https://nonexistent-url/image.jpg"

    #     # This should raise some kind of exception
    #     with self.assertRaises(Exception):  # Replace with your specific exception
    #         image_obj = ImageFactory.make_from_url(invalid_url)
    #         operator = self.feluda.operators.get()["image_vec_rep_resnet"]
    #         operator.run(image_obj)

    # def test_operator_configuration(self):
    #     """Test that operator is properly configured."""
    #     operator = self.feluda.operators.get()["image_vec_rep_resnet"]

    #     self.assertIsNotNone(operator, "Operator should be properly initialized")
    #     self.assertTrue(hasattr(operator, 'run'), "Operator should have 'run' method")

    #     # Check operator parameters if applicable
    #     if hasattr(operator, 'parameters'):
    #         self.assertEqual(operator.parameters.get('index_name'), 'image',
    #                        "Operator should have correct parameters")
