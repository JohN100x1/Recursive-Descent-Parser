from dataclasses import MISSING

import pytest

from dsl.models.exceptions import DSLRuntimeError
from dsl.models.representables.actions import ReturnAction
from dsl.models.representables.evaluables import (
    EvaluableAction,
    EvaluableActionArg,
    EvaluableBlock,
    EvaluableElifStatement,
    EvaluableExpression,
    EvaluableIfStatement,
    EvaluableList,
    EvaluableListArg,
)
from dsl.models.representables.keywords import (
    ElifKeyword,
    ElseKeyword,
    IfKeyword,
    ThenKeyword,
)
from dsl.models.representables.operands import BoolOperand, IntegerOperand
from dsl.models.representables.operators import (
    CountFunction,
    GreaterThanOperator,
    LessThanOperator,
    MultOperator,
    PlusOperator,
)


class TestEvaluable:
    """Test Evaluable."""

    def test_repr(self):
        evaluable = EvaluableAction(
            contents=[ReturnAction(), IntegerOperand("1")]
        )
        evaluable_repr = (
            "EvaluableAction([ReturnAction(), IntegerOperand('1')])"
        )
        assert evaluable.__repr__() == evaluable_repr

    def test_eq(self):
        evaluable_1 = EvaluableExpression(contents=[IntegerOperand("1")])
        evaluable_2 = EvaluableExpression(contents=[IntegerOperand("1")])
        evaluable_3 = 1
        assert evaluable_1 == evaluable_2
        assert evaluable_1 != evaluable_3 and evaluable_2 != evaluable_3


class TestEvaluableEvaluate:
    """Test Evaluable.evaluate."""

    def test_list_in_function(self):
        evaluable = EvaluableExpression(
            [
                CountFunction("COUNT("),
                EvaluableList(
                    [
                        BoolOperand("TRUE"),
                        EvaluableListArg(
                            [BoolOperand("FALSE"), BoolOperand("TRUE")]
                        ),
                    ]
                ),
            ]
        )
        assert evaluable.evaluate() == 2

    def test_list_in_list_arg(self):
        evaluable = EvaluableListArg(
            [
                IntegerOperand("1"),
                EvaluableList([IntegerOperand("2"), IntegerOperand("3")]),
            ]
        )
        assert evaluable.evaluate() == [1, 2, 3]

    def test_leftover_operator(self):
        evaluable = EvaluableExpression([PlusOperator("+")])
        with pytest.raises(
            DSLRuntimeError, match="Evaluation of Evaluable has left "
        ):
            evaluable.evaluate()

    def test_leftover_operands(self):
        evaluable = EvaluableExpression(
            [IntegerOperand("1"), IntegerOperand("2")]
        )
        with pytest.raises(
            DSLRuntimeError, match="not collapse to a single value."
        ):
            evaluable.evaluate()

    def test_simple_arithmetic(self):
        evaluable = EvaluableExpression(
            [IntegerOperand("1"), PlusOperator("+"), IntegerOperand("2")]
        )
        assert evaluable.evaluate()

    def test_order_of_operations(self):
        evaluable_1 = EvaluableExpression(
            [
                IntegerOperand("1"),
                PlusOperator("+"),
                EvaluableExpression(
                    [
                        IntegerOperand("2"),
                        MultOperator("*"),
                        IntegerOperand("3"),
                    ]
                ),
            ]
        )
        evaluable_2 = EvaluableExpression(
            [
                EvaluableExpression(
                    [
                        IntegerOperand("1"),
                        PlusOperator("+"),
                        IntegerOperand("2"),
                    ]
                ),
                MultOperator("*"),
                IntegerOperand("3"),
            ]
        )
        assert evaluable_1.evaluate() == 7
        assert evaluable_2.evaluate() == 9

    def test_return_action(self):
        evaluable_1 = EvaluableAction([ReturnAction(), IntegerOperand("123")])
        evaluable_2 = EvaluableAction(
            [
                ReturnAction(),
                IntegerOperand("4"),
                EvaluableActionArg([IntegerOperand("5"), IntegerOperand("6")]),
            ]
        )
        evaluable_3 = EvaluableAction(
            [
                ReturnAction(),
                IntegerOperand("7"),
                EvaluableActionArg(
                    [
                        IntegerOperand("8"),
                        EvaluableActionArg(
                            [IntegerOperand("9"), IntegerOperand("10")]
                        ),
                    ]
                ),
            ]
        )
        assert evaluable_1.evaluate() == 123
        assert evaluable_2.evaluate() == (4, 5, 6)
        assert evaluable_3.evaluate() == (7, 8, 9, 10)

    def test_invalid_action(self):
        evaluable = EvaluableAction([IntegerOperand("1")])
        with pytest.raises(DSLRuntimeError, match="is not a valid Action."):
            evaluable.evaluate()

    def test_if_statement(self):
        evaluable = EvaluableIfStatement(
            [
                IfKeyword(),
                EvaluableExpression(
                    [
                        IntegerOperand("3"),
                        GreaterThanOperator(">"),
                        IntegerOperand("2"),
                    ]
                ),
                ThenKeyword(),
                EvaluableAction([ReturnAction(), IntegerOperand("1")]),
            ]
        )
        assert evaluable.evaluate() == 1

    def test_elif_statement(self):
        evaluable = EvaluableIfStatement(
            [
                IfKeyword(),
                EvaluableExpression(
                    [
                        IntegerOperand("1"),
                        GreaterThanOperator(">"),
                        IntegerOperand("2"),
                    ]
                ),
                ThenKeyword(),
                EvaluableAction([ReturnAction(), IntegerOperand("1")]),
                EvaluableElifStatement(
                    [
                        ElifKeyword(),
                        EvaluableExpression(
                            [
                                IntegerOperand("5"),
                                LessThanOperator("<"),
                                IntegerOperand("6"),
                            ]
                        ),
                        ThenKeyword(),
                        EvaluableAction([ReturnAction(), IntegerOperand("9")]),
                    ]
                ),
            ]
        )
        assert evaluable.evaluate() == 9

    def test_else_statement(self):
        evaluable = EvaluableIfStatement(
            [
                IfKeyword(),
                BoolOperand("FALSE"),
                ThenKeyword(),
                EvaluableAction([ReturnAction(), IntegerOperand("1")]),
                EvaluableElifStatement(
                    [
                        ElseKeyword(),
                        EvaluableAction([ReturnAction(), IntegerOperand("7")]),
                    ]
                ),
            ]
        )
        assert evaluable.evaluate() == 7

    def test_two_if_statements(self):
        evaluable = EvaluableBlock(
            [
                EvaluableIfStatement(
                    [
                        IfKeyword(),
                        BoolOperand("TRUE"),
                        ThenKeyword(),
                        EvaluableAction([ReturnAction(), IntegerOperand("1")]),
                    ]
                ),
                EvaluableIfStatement(
                    [
                        IfKeyword(),
                        BoolOperand("TRUE"),
                        ThenKeyword(),
                        EvaluableAction([ReturnAction(), IntegerOperand("2")]),
                    ]
                ),
            ]
        )
        assert evaluable.evaluate() == [1, 2]

    def test_invalid_if_statement(self):
        evaluable_1 = EvaluableIfStatement()
        with pytest.raises(
            DSLRuntimeError, match="Cannot evaluate IF statement"
        ):
            evaluable_1.evaluate()

        evaluable_2 = EvaluableIfStatement([IfKeyword(), BoolOperand("TRUE")])
        with pytest.raises(
            DSLRuntimeError, match="Cannot evaluate IF statement"
        ):
            evaluable_2.evaluate()

    def test_extended_elif_statement(self):
        evaluable_1 = EvaluableElifStatement(
            [
                ElifKeyword(),
                BoolOperand("FALSE"),
                ThenKeyword(),
                EvaluableAction([ReturnAction(), IntegerOperand("1")]),
            ]
        )
        evaluable_2 = EvaluableElifStatement(
            [
                ElifKeyword(),
                BoolOperand("FALSE"),
                ThenKeyword(),
                EvaluableAction([ReturnAction(), IntegerOperand("1")]),
                EvaluableElifStatement(
                    [
                        ElifKeyword(),
                        BoolOperand("TRUE"),
                        ThenKeyword(),
                        EvaluableAction(
                            [ReturnAction(), IntegerOperand("157")]
                        ),
                    ]
                ),
            ]
        )
        evaluable_3 = EvaluableElifStatement(
            [
                ElifKeyword(),
                BoolOperand("TRUE"),
                ThenKeyword(),
                EvaluableAction([ReturnAction(), IntegerOperand("987")]),
                EvaluableElifStatement(),
            ]
        )
        assert evaluable_1.evaluate() is MISSING
        assert evaluable_2.evaluate() == 157
        assert evaluable_3.evaluate() == 987

    def test_invalid_elif_statement(self):
        evaluable = EvaluableElifStatement()
        with pytest.raises(
            DSLRuntimeError, match="Cannot evaluate ELIF statement"
        ):
            evaluable.evaluate()
