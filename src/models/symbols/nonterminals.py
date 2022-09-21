from typing import ClassVar, Type

from quac_core.dsl.models.representables.evaluables import (
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
from quac_core.dsl.models.symbols import NonTerminalSymbol


class BlockSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableBlock


class IfStatementSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableIfStatement


class ElifStatementSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableElifStatement


class ActionSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableAction


class ActionArgSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableActionArg


class EvaluableExpressionSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableExpression


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
    represents: ClassVar[Type[Evaluable]] = EvaluableList


class ListArgSymbol(NonTerminalSymbol):
    represents: ClassVar[Type[Evaluable]] = EvaluableListArg
