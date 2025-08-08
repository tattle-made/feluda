import pytest
from unittest.mock import patch, MagicMock
from feluda.operator import Operator

@pytest.fixture
def mock_config():
    return {'param': 'value'}

class TestOperator:
    def test_operator_init_sets_config(self, monkeypatch, mock_config):
        monkeypatch.setattr('feluda.operator.Operator.load_config', lambda self: mock_config)
        op = Operator()
        assert op.config == mock_config

    def test_operator_run_calls_process(self, monkeypatch):
        mock_process = MagicMock(return_value='result')
        monkeypatch.setattr(Operator, 'process', mock_process)
        op = Operator()
        result = op.run('input')
        mock_process.assert_called_once_with('input')
        assert result == 'result'

    def test_operator_process_handles_error(self, monkeypatch):
        op = Operator()
        monkeypatch.setattr(op, 'process', MagicMock(side_effect=Exception('fail')))
        with pytest.raises(Exception):
            op.run('bad input')
