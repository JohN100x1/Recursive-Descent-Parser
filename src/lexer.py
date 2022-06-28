import re
from typing import Any, Optional, Type

from models.exceptions import DSLSyntaxError
from models.symbols import TerminalSymbol
from models.symbols.terminals import (
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
    InvalidSymbol,
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


class Lexer:
    DEFAULT_BASE_SYMBOLS: list[Type[TerminalSymbol]] = [
        IndexingSymbol,
        LeftSquareBracketLiteral,
        RightSquareBracketLiteral,
        CommaLiteral,
        ReturnLiteral,
        IfLiteral,
        ElifLiteral,
        ThenLiteral,
        ElseLiteral,
        CountLiteral,
        DivLiteral,
        MultLiteral,
        ModLiteral,
        PlusLiteral,
        MinusLiteral,
        GreaterThanOrEqualLiteral,
        LessThanOrEqualLiteral,
        LessThanLiteral,
        GreaterThanLiteral,
        EqualLiteral,
        NotEqualLiteral,
        NotLiteral,
        AndLiteral,
        OrLiteral,
        LeftParenthesisLiteral,
        RightParenthesisLiteral,
        BoolLiteral,
        NoneLiteral,
        StringLiteral,
        AttributeSymbol,
        VariableSymbol,
        FloatLiteral,
        IntegerLiteral,
        InvalidSymbol,
    ]

    def __init__(
        self,
        variables: Optional[dict[str, Any]] = None,
        inclusions: Optional[list[Type[TerminalSymbol]]] = None,
        exclusions: Optional[list[Type[TerminalSymbol]]] = None,
        base_symbols: Optional[list[Type[TerminalSymbol]]] = None,
    ):
        self.variables = variables or {}

        symbols = {
            s.__name__: s for s in base_symbols or self.DEFAULT_BASE_SYMBOLS
        }
        self.inclusions = {s.__name__: s for s in inclusions or []} | symbols
        for symbol in exclusions or []:
            self.inclusions.pop(symbol.__name__, None)

        # Create a regex matching map of symbols regexes to their name
        regexes = [
            f"(?P<{name}>{sym.regex})" for name, sym in self.inclusions.items()
        ]
        self.pattern = re.compile(r"|".join(regexes))

    def tokenize(self, input_string: str) -> list[TerminalSymbol]:
        """
        Return a list of validated token objects from a given input string.
        :param input_string: The input_string to split.
        :return: A list of Tokens obtained by splitting the input string.
        """
        tokens = []
        for match in re.finditer(self.pattern, input_string):
            lexeme = match.group()
            symbol = self.inclusions[str(match.lastgroup)]
            if symbol == VariableSymbol:
                token = symbol(lexeme=lexeme, variables=self.variables)
            else:
                token = symbol(lexeme=lexeme)
            tokens.append(token)
        self.validate_tokens(tokens)
        return tokens

    @staticmethod
    def validate_tokens(tokens: list[TerminalSymbol]) -> None:
        """
        Validate a list of symbols to ensure symbols are valid.
        :param tokens: A list of token objects.
        :return: None
        """
        for token in tokens:
            # Disallow invalid symbols
            if isinstance(token, InvalidSymbol):
                raise DSLSyntaxError(f"Unknown syntax {token.lexeme}.")
