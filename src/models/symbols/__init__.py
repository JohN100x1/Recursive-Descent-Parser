from abc import ABC, abstractmethod
from collections import deque
from typing import Any, ClassVar, Iterable, MutableSequence, Optional, Type, Union

from quac_core.dsl.models.representables import Representable
from quac_core.dsl.models.representables.evaluables import Evaluable


class Symbol(ABC):
    pass


class TerminalSymbol(Symbol):
    regex: ClassVar[str]

    def __init__(self, lexeme: str, variables: dict[str, Any] | None = None):
        self.lexeme = lexeme
        self.variables = variables or {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.lexeme}')"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.lexeme == other.lexeme

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        if not hasattr(cls, "regex"):
            raise AttributeError(f"{cls.__name__} missing required attribute 'regex'.")

    @property
    @abstractmethod
    def represents(self) -> Representable:
        """:return: Object the terminal symbol represents."""
        ...


class NonTerminalSymbol(Symbol):
    represents: ClassVar[Type[Evaluable]]

    def __init__(self, contents: Iterable["TSymbol"] | None = None):
        self.contents: MutableSequence[TSymbol] = deque(contents or [])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self.contents)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.contents == other.contents

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        if not hasattr(cls, "represents"):
            err_msg = f"{cls.__name__} missing required attribute 'represents'."
            raise AttributeError(err_msg)


TSymbol = Union[TerminalSymbol, NonTerminalSymbol]
