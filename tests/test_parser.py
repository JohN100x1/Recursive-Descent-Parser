from parser import Parser

from models.symbols.nonterminals import (
    ExpressionSymbol,
    FactorSymbol,
    OperandSymbol,
    TermSymbol,
)
from models.symbols.terminals import IntegerLiteral, MultLiteral, PlusLiteral


def test_parser_expression():
    parser = Parser()
    parse_tree = parser.parse(
        [
            IntegerLiteral("1"),
            MultLiteral("*"),
            IntegerLiteral("2"),
            PlusLiteral("+"),
            IntegerLiteral("3"),
        ],
        start_symbol=ExpressionSymbol(),
    )
    assert parse_tree == [
        ExpressionSymbol(
            [
                TermSymbol(
                    [
                        FactorSymbol([OperandSymbol([IntegerLiteral("1")])]),
                        MultLiteral("*"),
                        ExpressionSymbol(
                            [
                                TermSymbol(
                                    [
                                        FactorSymbol(
                                            [
                                                OperandSymbol(
                                                    [IntegerLiteral("2")]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                PlusLiteral("+"),
                                ExpressionSymbol(
                                    [
                                        TermSymbol(
                                            [
                                                FactorSymbol(
                                                    [
                                                        OperandSymbol(
                                                            [
                                                                IntegerLiteral(
                                                                    "3"
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
