from abc import abstractmethod
from typing import Any, Optional

from dsl.models.exceptions import DSLException, DSLRuntimeError
from dsl.models.representables import Representable


class Operand(Representable):
    def __init__(
        self,
        token_value: str,
        variables: dict[str, Any] | None = None,
        value: Any = None,
    ):
        self.token_value = token_value
        self.variables = variables or {}
        self.value = value or []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.token_value}')"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Operand):
            return False
        if self.variables != other.variables:
            raise DSLException("Variable lookup tables do not match.")
        return self.token_value == other.token_value

    @property
    @abstractmethod
    def true_value(self) -> Any:
        """Get the true value of the operand."""
        ...


class NoneOperand(Operand):
    @property
    def true_value(self) -> Any:
        """Get the value of none token."""
        return None


class BoolOperand(Operand):
    @property
    def true_value(self) -> Any:
        """Get the value of bool token."""
        return self.token_value == "TRUE"


class StringOperand(Operand):
    @property
    def true_value(self) -> Any:
        """Get the value of string token."""
        return self.token_value.strip("'")


class VariableOperand(Operand):
    @property
    def true_value(self) -> Any:
        """Get the value of variable token."""
        try:
            return self.variables[self.token_value]
        except KeyError as err:
            raise DSLRuntimeError(
                f"{self.token_value} does not exist."
            ) from err


class FloatOperand(Operand):
    @property
    def true_value(self) -> float:
        """Get the float value of float token."""
        return float(self.token_value)


class IntegerOperand(Operand):
    @property
    def true_value(self) -> int:
        """Get the integer value of integer token."""
        return int(self.token_value)
