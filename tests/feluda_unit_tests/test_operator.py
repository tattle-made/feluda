import unittest
from unittest.mock import MagicMock, call, patch

from feluda.config import OperatorConfig, OperatorParameters
from feluda.operator import Operator


class TestOperator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.operator_params = [
            OperatorParameters(
                name="Test Operator 1",
                type="test_operator_1",
                parameters={"param1": "value1"},
            ),
            OperatorParameters(
                name="Test Operator 2",
                type="test_operator_2",
                parameters={"param2": "value2"},
            ),
        ]

        self.operator_config = MagicMock(spec=OperatorConfig)
        self.operator_config.parameters = self.operator_params

    def test_init(self):
        """Test Operator initialization"""
        operator = Operator(self.operator_config)

        self.assertEqual({}, operator.active_operators)
        self.assertEqual(self.operator_params, operator.operators)

    @patch("feluda.operator.importlib.import_module")
    def test_setup(self, mock_import_module):
        """Test Operator setup method"""
        mock_module1 = MagicMock()
        mock_module2 = MagicMock()

        mock_import_module.side_effect = [mock_module1, mock_module2]

        operator = Operator(self.operator_config)
        operator.setup()

        mock_import_module.assert_has_calls(
            [call("test_operator_1"), call("test_operator_2")]
        )

        mock_module1.initialize.assert_called_once_with({"param1": "value1"})
        mock_module2.initialize.assert_called_once_with({"param2": "value2"})

        self.assertEqual(2, len(operator.active_operators))
        self.assertEqual(mock_module1, operator.active_operators["test_operator_1"])
        self.assertEqual(mock_module2, operator.active_operators["test_operator_2"])

    @patch("feluda.operator.importlib.import_module")
    def test_setup_with_empty_operator_list(self, mock_import_module):
        """Test Operator setup method with an empty operator list"""
        empty_config = MagicMock(spec=OperatorConfig)
        empty_config.parameters = []

        operator = Operator(empty_config)
        operator.setup()

        mock_import_module.assert_not_called()
        self.assertEqual({}, operator.active_operators)

    def test_get(self):
        """Test Operator get method"""
        operator = Operator(self.operator_config)
        mock_module1 = MagicMock()
        mock_module2 = MagicMock()
        operator.active_operators = {
            "test_operator_1": mock_module1,
            "test_operator_2": mock_module2,
        }

        result = operator.get()

        self.assertEqual(2, len(result))
        self.assertEqual(mock_module1, result["test_operator_1"])
        self.assertEqual(mock_module2, result["test_operator_2"])

    @patch("feluda.operator.importlib.import_module")
    def test_setup_with_import_error(self, mock_import_module):
        """Test Operator setup method when import fails"""
        mock_import_module.side_effect = [ImportError("Module not found"), MagicMock()]

        operator = Operator(self.operator_config)

        with self.assertRaises(ImportError):
            operator.setup()

        self.assertEqual({}, operator.active_operators)

    @patch("feluda.operator.importlib.import_module")
    def test_setup_with_initialization_error(self, mock_import_module):
        """Test Operator setup method when module initialization fails"""
        mock_module = MagicMock()
        mock_module.initialize.side_effect = Exception("Initialization failed")
        mock_import_module.return_value = mock_module

        operator = Operator(self.operator_config)

        with self.assertRaises(Exception):
            operator.setup()

        self.assertEqual({}, operator.active_operators)
