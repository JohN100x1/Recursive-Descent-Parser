import pytest

from quac_core.dsl.models.exceptions import DSLException, DSLRuntimeError
from quac_core.dsl.models.representables.operands import (
    BoolOperand,
    FloatOperand,
    IntegerOperand,
    Operand,
    VariableOperand,
)


class TestOperand:
    """Test Operand."""

    def test_repr(self):
        class Bar(Operand):
            @property
            def true_value(self):
                return 1

        assert Bar("foo").__repr__() == "Bar('foo')"

    def test_not_eq(self):
        assert IntegerOperand("2") != 3

        with pytest.raises(DSLException):
            int_operand_1 = IntegerOperand("2", variables={"foo": 1})
            int_operand_2 = IntegerOperand("2", variables={"foo": 2})
            assert int_operand_1 != int_operand_2


def test_operands():
    variables = {"a": 1, "b": 0.2, "c": True}
    assert isinstance(VariableOperand("a", variables).true_value, int)
    assert isinstance(VariableOperand("b", variables).true_value, float)
    assert isinstance(VariableOperand("c", variables).true_value, bool)
    assert isinstance(IntegerOperand("2").true_value, int)
    assert isinstance(FloatOperand("2.3").true_value, float)
    assert BoolOperand("TRUE").true_value is True

    with pytest.raises(DSLRuntimeError, match="d does not exist."):
        assert VariableOperand("d", variables).true_value
