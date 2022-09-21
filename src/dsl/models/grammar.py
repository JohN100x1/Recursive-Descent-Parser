from typing import Any, Type

from dsl.models.symbols import NonTerminalSymbol, TSymbol
from dsl.models.symbols.nonterminals import (
    ActionArgSymbol,
    ActionSymbol,
    BlockSymbol,
    ConditionExprSymbol,
    ConditionFactorSymbol,
    ConditionSymbol,
    ConditionTermSymbol,
    ElifStatementSymbol,
    ExpressionSymbol,
    FactorSymbol,
    IfStatementSymbol,
    ListArgSymbol,
    ListSymbol,
    OperandSymbol,
    TermSymbol,
)
from dsl.models.symbols.terminals import (
    AndLiteral,
    AttributeSymbol,
    BoolLiteral,
    CommaLiteral,
    CountLiteral,
    DivLiteral,
    ElifLiteral,
    ElseLiteral,
    EqualLiteral,
    FloatLiteral,
    GreaterThanLiteral,
    GreaterThanOrEqualLiteral,
    IfLiteral,
    IndexingSymbol,
    IntegerLiteral,
    LeftParenthesisLiteral,
    LeftSquareBracketLiteral,
    LessThanLiteral,
    LessThanOrEqualLiteral,
    MinusLiteral,
    ModLiteral,
    MultLiteral,
    NoneLiteral,
    NotEqualLiteral,
    NotLiteral,
    OrLiteral,
    PlusLiteral,
    ReturnLiteral,
    RightParenthesisLiteral,
    RightSquareBracketLiteral,
    StringLiteral,
    ThenLiteral,
    VariableSymbol,
)


class Production:
    def __init__(self, *args: Type[TSymbol]):
        self.body = tuple(args)

    def __repr__(self) -> str:
        return f"Production({', '.join(s.__name__ for s in self.body)})"

    def __hash__(self) -> int:
        return hash(self.body)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.body == other.body


class Grammar(dict[Type[NonTerminalSymbol], list[Production]]):
    pass


base_grammar = Grammar(
    {
        BlockSymbol: [
            Production(IfStatementSymbol, BlockSymbol),
            Production(IfStatementSymbol),
        ],
        IfStatementSymbol: [
            Production(
                IfLiteral,
                ConditionExprSymbol,
                ThenLiteral,
                ActionSymbol,
                ElifStatementSymbol,
            ),
            Production(
                IfLiteral, ConditionExprSymbol, ThenLiteral, ActionSymbol
            ),
        ],
        ElifStatementSymbol: [
            Production(ElseLiteral, ActionSymbol),
            Production(
                ElifLiteral,
                ConditionExprSymbol,
                ThenLiteral,
                ActionSymbol,
                ElifStatementSymbol,
            ),
            Production(
                ElifLiteral, ConditionExprSymbol, ThenLiteral, ActionSymbol
            ),
        ],
        ActionSymbol: [
            Production(ReturnLiteral, OperandSymbol, RightParenthesisLiteral),
            Production(ReturnLiteral, OperandSymbol, ActionArgSymbol),
        ],
        ActionArgSymbol: [
            Production(CommaLiteral, OperandSymbol, RightParenthesisLiteral),
            Production(CommaLiteral, OperandSymbol, ActionArgSymbol),
        ],
        ConditionExprSymbol: [
            Production(ConditionTermSymbol, OrLiteral, ConditionExprSymbol),
            Production(ConditionTermSymbol),
        ],
        ConditionTermSymbol: [
            Production(ConditionFactorSymbol, AndLiteral, ConditionExprSymbol),
            Production(ConditionFactorSymbol),
        ],
        ConditionFactorSymbol: [
            Production(NotLiteral, ConditionSymbol),
            Production(BoolLiteral),
            Production(ConditionSymbol),
        ],
        ConditionSymbol: [
            Production(ExpressionSymbol, EqualLiteral, ConditionSymbol),
            Production(ExpressionSymbol, NotEqualLiteral, ConditionSymbol),
            Production(ExpressionSymbol, GreaterThanLiteral, ConditionSymbol),
            Production(ExpressionSymbol, LessThanLiteral, ConditionSymbol),
            Production(
                ExpressionSymbol, LessThanOrEqualLiteral, ConditionSymbol
            ),
            Production(
                ExpressionSymbol, GreaterThanOrEqualLiteral, ConditionSymbol
            ),
            Production(ExpressionSymbol),
        ],
        ExpressionSymbol: [
            Production(TermSymbol, PlusLiteral, ExpressionSymbol),
            Production(TermSymbol, MinusLiteral, ExpressionSymbol),
            Production(TermSymbol),
        ],
        TermSymbol: [
            Production(FactorSymbol, MultLiteral, ExpressionSymbol),
            Production(FactorSymbol, DivLiteral, ExpressionSymbol),
            Production(FactorSymbol, ModLiteral, ExpressionSymbol),
            Production(FactorSymbol),
        ],
        FactorSymbol: [
            Production(
                CountLiteral, ConditionExprSymbol, RightParenthesisLiteral
            ),
            Production(VariableSymbol, AttributeSymbol, AttributeSymbol),
            Production(VariableSymbol, IndexingSymbol, AttributeSymbol),
            Production(VariableSymbol, AttributeSymbol),
            Production(VariableSymbol, IndexingSymbol),
            Production(OperandSymbol),
            Production(
                LeftParenthesisLiteral,
                ConditionSymbol,
                RightParenthesisLiteral,
            ),
        ],
        OperandSymbol: [
            Production(VariableSymbol),
            Production(IntegerLiteral),
            Production(FloatLiteral),
            Production(StringLiteral),
            Production(BoolLiteral),
            Production(NoneLiteral),
            Production(ListSymbol),
        ],
        ListSymbol: [
            Production(
                LeftSquareBracketLiteral,
                OperandSymbol,
                RightSquareBracketLiteral,
            ),
            Production(LeftSquareBracketLiteral, OperandSymbol, ListArgSymbol),
        ],
        ListArgSymbol: [
            Production(CommaLiteral, OperandSymbol, RightSquareBracketLiteral),
            Production(CommaLiteral, OperandSymbol, ListArgSymbol),
        ],
    }
)
