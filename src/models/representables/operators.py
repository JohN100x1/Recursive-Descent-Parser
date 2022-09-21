from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar, Iterable

from quac_core.dsl.models.representables import Representable


class Operator(Representable):
    precedence: ClassVar[int]
    registrable: ClassVar[bool] = True

    def __init__(self, token_value: str):
        self.token_value = token_value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.token_value}')"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Operator):
            return False
        return self.__class__.__name__ == other.__class__.__name__

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        if not cls.registrable:
            return
        if not hasattr(cls, "precedence"):
            err_msg = f"{cls.__name__} missing required attribute 'precedence'."
            raise AttributeError(err_msg)


class UnitaryOperator(Operator):
    registrable: ClassVar[bool] = False

    @abstractmethod
    def evaluate(self, x: Any) -> Any:
        """A function takes in one argument."""
        ...


class BinaryOperator(Operator):
    registrable: ClassVar[bool] = False

    @abstractmethod
    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using an operation."""
        ...


class IndexingOperator(UnitaryOperator):
    precedence: ClassVar[int] = 6
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any) -> Any:
        """Evaluate input x using operation."""
        return x[int(self.token_value[1:-1]) - 1]


class AttributeOperator(UnitaryOperator):
    precedence: ClassVar[int] = 6
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any) -> Any:
        """Evaluate input x using operation."""
        attr = self.token_value.split(".", 1)[1]
        if isinstance(x, list):
            return [y[attr] if isinstance(y, dict) else getattr(y, attr) for y in x]
        if isinstance(x, dict):
            return x[attr]
        return getattr(x, attr)


class DivOperator(BinaryOperator):
    precedence: ClassVar[int] = 5
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using division operation."""
        return x / y


class MultOperator(BinaryOperator):
    precedence: ClassVar[int] = 5
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using multiplication operation."""
        return x * y


class ModOperator(BinaryOperator):
    precedence: ClassVar[int] = 5
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using modulus operation."""
        return x % y


class PlusOperator(BinaryOperator):
    precedence: ClassVar[int] = 4
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using plus operation."""
        return x + y


class MinusOperator(BinaryOperator):
    precedence: ClassVar[int] = 4
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using minus operation."""
        return x - y


class GreaterThanOrEqualOperator(BinaryOperator):
    precedence: ClassVar[int] = 3
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using greater than or equal to operation."""
        return x >= y


class LessThanOrEqualOperator(BinaryOperator):
    precedence: ClassVar[int] = 3
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using less than or equal to operation."""
        return x <= y


class LessThanOperator(BinaryOperator):
    precedence: ClassVar[int] = 3
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using less than operation."""
        return x < y


class GreaterThanOperator(BinaryOperator):
    precedence: ClassVar[int] = 3
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using greater than operation."""
        return x > y


class EqualOperator(BinaryOperator):
    precedence: ClassVar[int] = 3
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using equal to operation."""
        if isinstance(x, list) and isinstance(y, list):
            return [i == j for i, j in zip(x, y)]
        if isinstance(x, list) and not isinstance(y, list):
            return [i == y for i in x]
        if isinstance(y, list) and not isinstance(x, list):
            return [j == x for j in y]
        return x == y


class NotEqualOperator(BinaryOperator):
    precedence: ClassVar[int] = 3
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using not equal to operation."""
        if isinstance(x, list) and isinstance(y, list):
            return [i != j for i, j in zip(x, y)]
        if isinstance(x, list) and not isinstance(y, list):
            return [i != y for i in x]
        if isinstance(y, list) and not isinstance(x, list):
            return [j != x for j in y]
        return x != y


class NotOperator(UnitaryOperator):
    precedence: ClassVar[int] = 2
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any) -> Any:
        """Evaluate input x using NOT operation."""
        if isinstance(x, list):
            return [not y for y in x]
        return not x


class AndOperator(BinaryOperator):
    precedence: ClassVar[int] = 1
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using AND operation."""
        if isinstance(x, list) and isinstance(y, list):
            return [i and j for i, j in zip(x, y)]
        return x and y


class OrOperator(BinaryOperator):
    precedence: ClassVar[int] = 0
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Any, y: Any) -> Any:
        """Evaluate inputs x and y using OR operation."""
        if isinstance(x, list) and isinstance(y, list):
            return [i or j for i, j in zip(x, y)]
        return x or y


class Function(UnitaryOperator, metaclass=ABCMeta):
    registrable: ClassVar[bool] = False


class CountFunction(Function):
    precedence: ClassVar[int] = -1
    registrable: ClassVar[bool] = True

    def evaluate(self, x: Iterable[bool]) -> Any:
        """Evaluate iterable input using the count operation."""
        return sum(x)
