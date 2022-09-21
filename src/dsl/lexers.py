import re
from abc import ABC, abstractmethod
from typing import Any, ClassVar

from dsl.models.exceptions import DSLSyntaxError
from dsl.models.symbols import TerminalSymbol
from dsl.models.symbols.terminals import (
    AndLiteral,
    AttributeLiteral,
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
    IndexingLiteral,
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
    VariableLiteral,
)


class Lexer(ABC):
    DEFAULT_BASE_SYMBOLS: ClassVar[list[type[TerminalSymbol]]] = [
        IndexingLiteral,
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
        AttributeLiteral,
        VariableLiteral,
        FloatLiteral,
        IntegerLiteral,
        InvalidSymbol,
    ]

    @abstractmethod
    def tokenize(self, input_string: str) -> list[TerminalSymbol]:
        """Return a list of terminals for a given input string."""
        ...


class DefaultLexer(Lexer):
    def __init__(
        self,
        variables: dict[str, Any] | None = None,
        inclusions: list[type[TerminalSymbol]] | None = None,
        exclusions: list[type[TerminalSymbol]] | None = None,
        base_symbols: list[type[TerminalSymbol]] | None = None,
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
        Return a list of validated token objects from a given input string
        :param input_string: The input_string to split.
        :return: A list of Tokens obtained by splitting the input string.
        """
        tokens = []
        for match in re.finditer(self.pattern, input_string):
            lexeme = match.group()
            symbol = self.inclusions[str(match.lastgroup)]
            if symbol == VariableLiteral:
                token = symbol(lexeme=lexeme, variables=self.variables)
            else:
                token = symbol(lexeme=lexeme)
            tokens.append(token)
        self.validate_tokens(tokens)
        return tokens

    @staticmethod
    def validate_tokens(tokens: list[TerminalSymbol]) -> None:
        """
        Validate a list of symbols to ensure symbols are valid
        :param tokens: A list of token objects.
        :return: None
        """
        for token in tokens:
            # Disallow invalid symbols
            if isinstance(token, InvalidSymbol):
                raise DSLSyntaxError(f"Unknown syntax {token.lexeme}.")
