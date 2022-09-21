from typing import Any, ClassVar

from quac_core.dsl.models.representables import Representable


class Punctuator(Representable):
    precedence: ClassVar[int]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Punctuator):
            return False
        return self.__class__.__name__ == other.__class__.__name__

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        if not hasattr(cls, "precedence"):
            err_msg = f"{cls.__name__} missing required attribute 'precedence'."
            raise AttributeError(err_msg)


class LeftParenthesis(Punctuator):
    precedence: ClassVar[int] = -1


class RightParenthesis(Punctuator):
    precedence: ClassVar[int] = -1


class CommaPunctuator(Punctuator):
    precedence: ClassVar[int] = -1


class LeftSquareBracket(Punctuator):
    precedence: ClassVar[int] = -1


class RightSquareBracket(Punctuator):
    precedence: ClassVar[int] = -1
