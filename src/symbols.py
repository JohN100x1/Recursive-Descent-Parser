from abc import ABC, abstractmethod
from typing import Type


class Symbol(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__


# Production
class Production:
    def __init__(self, *args: Type[Symbol]):
        self.body = list(args)

    def contents(self) -> str:
        return ", ".join(s.__name__ for s in self.body)


class TerminalSymbol(Symbol):
    def __init__(self, lexeme: str):
        self.lexeme = lexeme


class NonTerminalSymbol(Symbol):
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
class TermSymbol(NonTerminalSymbol):
    @property
    def productions(self) -> list[Production]:
        return [
            Production(FactorSymbol, PlusLiteral, FactorSymbol),
            Production(FactorSymbol),
        ]


class FactorSymbol(NonTerminalSymbol):
    @property
    def productions(self) -> list[Production]:
        return [Production(IntegerLiteral)]
