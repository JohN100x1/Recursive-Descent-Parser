from abc import abstractmethod
from typing import Any, ClassVar

from quac_core.dsl.models.representables import Representable


class Action(Representable):
    precedence: ClassVar[int] = -1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Action):
            return False
        return self.__class__.__name__ == other.__class__.__name__

    @abstractmethod
    def validate_args(self, *args: Any) -> bool:
        """Validates the arguments"""
        ...

    @abstractmethod
    def execute(self, *args: Any) -> Any:
        """Execute the action."""
        ...


class ReturnAction(Action):
    def validate_args(self, *args: Any) -> bool:
        """Validates the arguments"""
        return True

    def execute(self, *args: Any) -> Any:
        """Return the value x."""
        if len(args) == 1:
            return args[0]
        return args
