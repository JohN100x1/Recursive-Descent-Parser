from typing import ClassVar

from dsl.models.representables.evaluables import (
    Evaluable,
    EvaluableAction,
    EvaluableActionArg,
    EvaluableBlock,
    EvaluableElifStatement,
    EvaluableExpression,
    EvaluableIfStatement,
    EvaluableList,
    EvaluableListArg,
)
from dsl.models.symbols import NonTerminalSymbol


class BlockSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableBlock


class IfStatementSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableIfStatement


class ElifStatementSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableElifStatement


class ActionSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableAction


class ActionArgSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableActionArg


class EvaluableExpressionSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableExpression


class ConditionExprSymbol(EvaluableExpressionSymbol):
    pass


class ConditionTermSymbol(EvaluableExpressionSymbol):
    pass


class ConditionFactorSymbol(EvaluableExpressionSymbol):
    pass


class ConditionSymbol(EvaluableExpressionSymbol):
    pass


class ExpressionSymbol(EvaluableExpressionSymbol):
    pass


class TermSymbol(EvaluableExpressionSymbol):
    pass


class FactorSymbol(EvaluableExpressionSymbol):
    pass


class OperandSymbol(EvaluableExpressionSymbol):
    pass


class ListSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableList


class ListArgSymbol(NonTerminalSymbol):
    represents: ClassVar[type[Evaluable]] = EvaluableListArg
