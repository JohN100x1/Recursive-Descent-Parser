import pytest

from quac_core.dsl.models import Operator
from quac_core.dsl.models.representables.operators import (
    AndOperator,
    AttributeOperator,
    CountFunction,
    DivOperator,
    EqualOperator,
    GreaterThanOperator,
    GreaterThanOrEqualOperator,
    LessThanOperator,
    LessThanOrEqualOperator,
    MinusOperator,
    ModOperator,
    MultOperator,
    NotEqualOperator,
    NotOperator,
    OrOperator,
    PlusOperator,
)


class TestOperator:
    """Test Operator."""

    def test_eq(self):
        assert EqualOperator("==") == EqualOperator("==")
        assert EqualOperator("==") != "foo"

    def test_repr(self):
        class Bar(Operator):
            precedence = 1

        assert Bar("foo").__repr__() == "Bar('foo')"

    def test_no_precedence(self):
        with pytest.raises(AttributeError, match="precedence"):

            class Bar(Operator):
                pass

            assert Bar


def test_operators():
    # Test Binary operators
    assert DivOperator("/").evaluate(6, 2) == 3
    assert MultOperator("*").evaluate(6, 2) == 12
    assert ModOperator("%").evaluate(6, 2) == 0
    assert PlusOperator("+").evaluate(6, 2) == 8
    assert MinusOperator("-").evaluate(6, 2) == 4
    assert GreaterThanOrEqualOperator(">=").evaluate(3, 2) is True
    assert LessThanOrEqualOperator("<=").evaluate(3, 2) is False
    assert LessThanOperator("<").evaluate(3, 2) is False
    assert GreaterThanOperator(">").evaluate(3, 2) is True
    assert EqualOperator("==").evaluate(3, 3) is True
    assert NotEqualOperator("!=").evaluate(3, 3) is False
    assert AndOperator("AND").evaluate(False, True) is False
    assert OrOperator("OR").evaluate(False, True) is True

    # Test Unitary operators
    assert NotOperator("NOT").evaluate(False) is True
    assert AttributeOperator(".token_value").evaluate(AttributeOperator(".a")) == ".a"

    # Test functions
    assert CountFunction("COUNT(").evaluate([False, True]) == 1


def test_equal_operator_list():
    operator = EqualOperator("==")
    assert operator.evaluate([1, 2, 2], 2) == [False, True, True]
    assert operator.evaluate(2, [1, 2, 2]) == [False, True, True]
    assert operator.evaluate([1, 1, 2], [1, 2, 2]) == [True, False, True]


def test_not_equal_operator_list():
    operator = NotEqualOperator("!=")
    assert operator.evaluate([1, 1, 2], 2) == [True, True, False]
    assert operator.evaluate(2, [1, 1, 2]) == [True, True, False]
    assert operator.evaluate([1, 1, 2], [1, 2, 2]) == [False, True, False]


def test_not_operator_list():
    operator = NotOperator("NOT")
    assert operator.evaluate([True, False]) == [False, True]


def test_and_operator_list():
    operator = AndOperator("AND")
    bool_list_1, bool_list_2 = [True, True, False, False], [True, False, True, False]
    assert operator.evaluate(bool_list_1, bool_list_2) == [True, False, False, False]


def test_or_operator_list():
    operator = OrOperator("OR")
    bool_list_1, bool_list_2 = [True, True, False, False], [True, False, True, False]
    assert operator.evaluate(bool_list_1, bool_list_2) == [True, True, True, False]


def test_attribute_operator_list():
    operator = AttributeOperator(".z")
    assert operator.evaluate([{"z": 1}, {"z": 2}, {"z": 3}]) == [1, 2, 3]
    assert operator.evaluate([{"z": "a"}, {"z": "b"}, {"z": "c"}]) == ["a", "b", "c"]
