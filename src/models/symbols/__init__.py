from abc import ABC
from collections import deque
from typing import Any, MutableSequence, Optional, Union


class Symbol(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__


class TerminalSymbol(Symbol):
    regex: str

    def __init__(
        self, lexeme: str, variables: Optional[dict[str, Any]] = None
    ):
        self.lexeme = lexeme
        self.variables = variables or {}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.lexeme == other.lexeme

    def __repr__(self) -> str:
        return f"{self.name}('{self.lexeme}')"

    def __init_subclass__(cls, **kwargs: Any):
        if not hasattr(cls, "regex"):
            raise AttributeError(f"{cls.__name__} missing 'regex' attribute.")


class NonTerminalSymbol(Symbol):
    def __init__(self, contents: Optional[MutableSequence["TSymbol"]] = None):
        self.contents = deque(contents or [])

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.contents == other.contents

    def __repr__(self) -> str:
        return f"{self.name}({list(self.contents)})"


TSymbol = Union[NonTerminalSymbol, TerminalSymbol]
