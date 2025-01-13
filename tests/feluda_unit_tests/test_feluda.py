import os
import unittest
from unittest.mock import MagicMock, patch

import yaml


class TestFeluda(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # temporary config data structure for testing
        self.config_data = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "Dimension Reduction",
                        "type": "dimension_reduction",
                        "parameters": {"index_name": "video"},
                    },
                    {
                        "name": "Video Vector Representation",
                        "type": "vid_vec_rep_clip",
                        "parameters": {"index_name": "video"},
                    },
                ],
            }
        }

        # Mock config path
        self.config_path = "tests/feluda_unit_tests/test-feluda-config.yml"

    @patch("feluda.config.load")
    def test_init_with_operators(self, mock_config_load):
        """Test Feluda initialization with operators configuration."""
        # Configure the mock
        mock_config = MagicMock()
        operators_mock = MagicMock()
        operators_mock.parameters = self.config_data["operators"]["parameters"]
        mock_config.operators = operators_mock
        mock_config_load.return_value = mock_config

        # Initialize Feluda
        from feluda import Feluda

        feluda = Feluda(self.config_path)

        self.assertIsNotNone(feluda.config)
        self.assertIsNone(feluda.store)
        self.assertIsNotNone(feluda.operators)
        mock_config_load.assert_called_once_with(self.config_path)

    @patch("feluda.config.load")
    def test_init_without_operators(self, mock_config_load):
        """Test Feluda initialization without operators configuration."""
        # Configure the mock
        mock_config = MagicMock()
        mock_config.operators = None
        mock_config_load.return_value = mock_config

        # Initialize Feluda
        from feluda import Feluda

        feluda = Feluda(self.config_path)

        # Assertions
        self.assertIsNotNone(feluda.config)
        self.assertIsNone(feluda.store)
        self.assertIsNone(feluda.operators)

    @patch("feluda.config.load")
    @patch("feluda.operator.Operator.setup")
    def test_setup_with_operators(self, mock_operator_setup, mock_config_load):
        """Test setup method when operators are configured."""
        # Create a mock OperatorConfig
        mock_operator_config = MagicMock()
        mock_operator_config.parameters = self.config_data["operators"]["parameters"]

        # Configure the mock config
        mock_config = MagicMock()
        mock_config.operators = mock_operator_config
        mock_config_load.return_value = mock_config

        # Initialize and setup Feluda
        from feluda import Feluda

        feluda = Feluda(self.config_path)
        feluda.setup()

        # Assert that operator setup was called
        mock_operator_setup.assert_called_once()

    def test_config_file_loading(self):
        """Test actual config file loading."""
        # Write test config to file
        with open(self.config_path, "w") as f:
            yaml.dump(self.config_data, f)

        try:
            # Initialize Feluda with actual file
            from feluda import Feluda

            feluda = Feluda(self.config_path)

            # Assertions
            self.assertIsNotNone(feluda.config)
            self.assertIsNotNone(feluda.operators)
        finally:
            # Cleanup
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
