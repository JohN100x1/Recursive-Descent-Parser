from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from dsl.lexers import DefaultLexer, Lexer
from dsl.models import Grammar
from dsl.models.exceptions import DSLSyntaxError, DSLValidationError
from dsl.models.representables.actions import Action
from dsl.models.representables.evaluables import (
    Evaluable,
    EvaluableAction,
    EvaluableList,
)
from dsl.models.representables.operands import Operand
from dsl.models.symbols import NonTerminalSymbol
from dsl.parsers import DefaultParser, Parser


@dataclass
class ValidationResult:
    """
    Validation result object containing the possible outputs and error.
    """

    is_valid: bool
    actions: list[EvaluableAction] = field(default_factory=list)
    error: Exception | None = None


class AbstractDSL(ABC):
    @abstractmethod
    def validate(self, input_string: str) -> ValidationResult:
        """Validate the DSL and return a validation result object."""
        ...

    @abstractmethod
    def execute(self, input_string: str) -> list[Any]:
        """Execute the construct and return the outputs."""
        ...


class DefaultDSL(AbstractDSL):
    def __init__(
        self,
        lexer: Lexer | None = None,
        parser: Parser | None = None,
        start_symbol: NonTerminalSymbol | None = None,
    ):
        self.lexer = lexer or DefaultLexer()
        self.parser = parser or DefaultParser()
        self.start_symbol = start_symbol

    def construct(self, input_string: str) -> Evaluable:
        """
        Convert a list of Tokens into a list of Tokens and expressions
        :param input_string: An input string.
        :return: A list of nested non-terminal and terminal symbols.
        """
        tokens = self.lexer.tokenize(input_string)
        parse_tree = self.parser.parse(tokens, start_symbol=self.start_symbol)
        execution_tree = self.parser.reduce(parse_tree[0])[0]
        if not isinstance(execution_tree, Evaluable):
            raise DSLValidationError(f"{execution_tree=} is not an Evaluable.")
        return execution_tree

    def validate(self, input_string: str) -> ValidationResult:
        """
        Validate the DefaultDSL and return a validation result object
        :param input_string: An input string.
        :return: The result of the validation.
        """
        try:
            execution_tree = self.construct(input_string)
            actions = self.get_actions(execution_tree)
            return ValidationResult(True, actions=actions)
        except (DSLSyntaxError, DSLValidationError) as err:
            return ValidationResult(False, error=err)

    def execute(self, input_string: str) -> list[Any]:
        """
        Execute the construct and return the outcome
        :param input_string: An input string.
        :return: The outcome from executing the DefaultDSL.
        """
        execution_tree = self.construct(input_string)
        return execution_tree.evaluate()

    def get_actions(self, evaluable: Evaluable) -> list[EvaluableAction]:
        """
        Get a list of evaluable actions.
        :param evaluable: Evaluable object, contains evaluable/representable
        :return: A list of evaluable action objects
        """
        actions = []
        for item in evaluable.contents:
            if isinstance(item, EvaluableAction):
                self.validate_action(item)
                actions.append(item)
            elif isinstance(item, Evaluable):
                actions.extend(self.get_actions(item))
        return actions

    @staticmethod
    def validate_action(action: EvaluableAction):
        """
        Validate an Evaluable action and raises an error if the args are not
        valid for the action
        :param action: An EvaluableAction object.
        :return: None, raises an error if args are invalid.
        """
        act: Action = action.contents[0]
        args: list[Operand | EvaluableList] = action.contents[1:]
        evaluated_args: list[Any] = []
        for arg in args:
            if isinstance(arg, Operand):
                evaluated_args.append(arg.true_value)
            elif isinstance(arg, EvaluableList):
                evaluated_args.append(arg.evaluate())
        if act.validate_args(*evaluated_args):
            return
        raise DSLValidationError(f"Action {act} has invalid arguments {args}.")
