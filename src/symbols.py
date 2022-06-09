from abc import ABC, abstractmethod
from typing import Optional, Type, Union


class Symbol(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__


# Production
class Production:
    def __init__(self, *args: Type["TSymbol"]):
        self.body = list(args)

    def symbols(self) -> str:
        return ", ".join(s.__name__ for s in self.body)


class TerminalSymbol(Symbol):
    def __init__(self, lexeme: str):
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.lexeme})"


class NonTerminalSymbol(Symbol):
    def __init__(self, contents: Optional[list["TSymbol"]] = None):
        self.contents = contents or []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.contents})"

    @property
    @abstractmethod
    def productions(self) -> list[Production]:
        ...


# Terminals
class IntegerLiteral(TerminalSymbol):
    pass


class PlusLiteral(TerminalSymbol):
    def __init__(self, lexeme: str = "+"):
        super().__init__(lexeme)


class MultLiteral(TerminalSymbol):
    def __init__(self, lexeme: str = "*"):
        super().__init__(lexeme)


# Non-terminals
class ExpressionSymbol(NonTerminalSymbol):
    @property
    def productions(self) -> list[Production]:
        return [
            Production(TermSymbol, PlusLiteral, ExpressionSymbol),
            Production(TermSymbol),
        ]


class TermSymbol(NonTerminalSymbol):
    @property
    def productions(self) -> list[Production]:
        return [
            Production(FactorSymbol, MultLiteral, ExpressionSymbol),
            Production(FactorSymbol),
        ]


class FactorSymbol(NonTerminalSymbol):
    @property
    def productions(self) -> list[Production]:
        return [Production(IntegerLiteral)]


TSymbol = Union[NonTerminalSymbol, TerminalSymbol]
