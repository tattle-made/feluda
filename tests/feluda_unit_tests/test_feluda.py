from unittest.mock import MagicMock, patch

from feluda import Feluda


class TestFeluda:
    """Test class for Feluda framework."""

    def test_init_with_config(self):
        """Test Feluda initialization with configuration."""
        with patch("feluda.config.load") as mock_config_load:
            mock_config = MagicMock()
            mock_config.operators = None
            mock_config.store = None
            mock_config_load.return_value = mock_config

            feluda = Feluda("test_config.yml")

            assert feluda.config is not None
            assert feluda.store is None
            assert feluda.operators is None
            mock_config_load.assert_called_once_with("test_config.yml")

    def test_feluda_attributes(self):
        """Test that Feluda has the expected attributes."""
        with patch("feluda.config.load") as mock_config_load:
            mock_config = MagicMock()
            mock_config.operators = None
            mock_config.store = None
            mock_config_load.return_value = mock_config

            feluda = Feluda("test_config.yml")

            assert hasattr(feluda, "config")
            assert hasattr(feluda, "store")
            assert hasattr(feluda, "operators")
            assert feluda.store is None
            assert feluda.operators is None
