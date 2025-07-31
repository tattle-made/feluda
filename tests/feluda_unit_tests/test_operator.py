import pytest

from feluda.operator import Operator


class TestOperator:
    """Test class for Operator base class."""

    def test_operator_abstract_methods(self):
        """Test that Operator is an abstract base class and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Operator()

    def test_operator_has_required_methods(self):
        """Test that Operator defines the required abstract methods."""
        # Check that abstract methods exist and are marked abstract
        assert hasattr(Operator, "run")
        assert getattr(Operator.run, "__isabstractmethod__", False)

        assert hasattr(Operator, "cleanup")
        assert getattr(Operator.cleanup, "__isabstractmethod__", False)

        assert hasattr(Operator, "state")
        assert getattr(Operator.state, "__isabstractmethod__", False)

    def test_operator_inheritance(self):
        """Test that Operator inherits from ABC."""
        from abc import ABC

        assert issubclass(Operator, ABC)

    def test_operator_concrete_implementation(self):
        """Test that a concrete implementation of Operator works correctly."""

        class ConcreteOperator(Operator):
            def run(self, file_path: str, *args, **kwargs):
                return {"result": "test"}

            def cleanup(self) -> None:
                pass

            def state(self) -> dict:
                return {"status": "ready"}

        operator = ConcreteOperator()
        result = operator.run("test.txt")
        assert result["result"] == "test"

        state = operator.state()
        assert state["status"] == "ready"

        operator.cleanup()  # Should not raise an exception
