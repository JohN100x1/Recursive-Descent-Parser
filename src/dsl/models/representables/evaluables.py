from abc import abstractmethod
from collections import deque
from dataclasses import MISSING
from typing import Any

from dsl.models.exceptions import DSLRuntimeError
from dsl.models.representables import Representable
from dsl.models.representables.actions import Action
from dsl.models.representables.keywords import (
    ElifKeyword,
    ElseKeyword,
    IfKeyword,
    ThenKeyword,
)
from dsl.models.representables.operands import Operand
from dsl.models.representables.operators import BinaryOperator, UnitaryOperator


class Evaluable(Representable):
    def __init__(self, contents: list[Representable] | None = None):
        self.contents = contents or []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.contents})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Evaluable):
            return False
        return (
            self.contents == other.contents
            and self.__class__.__name__ == other.__class__.__name__
        )

    @abstractmethod
    def evaluate(self) -> Any:
        """Evaluate the contents of the Evaluable."""
        ...


class EvaluableBlock(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the contents of the Evaluable."""
        outputs = []
        for item in self.contents:
            output = item.evaluate()
            if (
                isinstance(item, EvaluableIfStatement)
                and output is not MISSING
            ):
                outputs.append(output)
            elif isinstance(item, EvaluableBlock) and output:
                outputs.extend(output)
        return outputs


class EvaluableIfStatement(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the contents of the IF statement."""
        condition: EvaluableExpression
        action: EvaluableAction
        elif_statement: EvaluableElifStatement
        match self.contents:
            case [
                IfKeyword(),
                EvaluableExpression() | Operand() as condition,
                ThenKeyword(),
                EvaluableAction() as action,
            ]:
                if (
                    isinstance(condition, Operand)
                    and condition.true_value
                    or isinstance(condition, EvaluableExpression)
                    and condition.evaluate()
                ):
                    return action.evaluate()
                else:
                    return MISSING
            case [
                IfKeyword(),
                EvaluableExpression() | Operand() as condition,
                ThenKeyword(),
                EvaluableAction() as action,
                EvaluableElifStatement() as elif_statement,
            ]:
                if (
                    isinstance(condition, Operand)
                    and condition.true_value
                    or isinstance(condition, EvaluableExpression)
                    and condition.evaluate()
                ):
                    return action.evaluate()
                else:
                    return elif_statement.evaluate()
            case _:
                raise DSLRuntimeError(
                    f"Cannot evaluate IF statement {self.contents}."
                )


class EvaluableElifStatement(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the contents of the ELIF statement."""
        condition: EvaluableExpression
        action: EvaluableAction
        elif_statement: EvaluableElifStatement
        match self.contents:
            case [ElseKeyword(), EvaluableAction() as action]:
                return action.evaluate()
            case [
                ElifKeyword(),
                EvaluableExpression() | Operand() as condition,
                ThenKeyword(),
                EvaluableAction() as action,
            ]:
                if (
                    isinstance(condition, Operand)
                    and condition.true_value
                    or isinstance(condition, EvaluableExpression)
                    and condition.evaluate()
                ):
                    return action.evaluate()
                else:
                    return MISSING
            case [
                ElifKeyword(),
                EvaluableExpression() | Operand() as condition,
                ThenKeyword(),
                EvaluableAction() as action,
                EvaluableElifStatement() as elif_statement,
            ]:
                if (
                    isinstance(condition, Operand)
                    and condition.true_value
                    or isinstance(condition, EvaluableExpression)
                    and condition.evaluate()
                ):
                    return action.evaluate()
                else:
                    return elif_statement.evaluate()
            case _:
                raise DSLRuntimeError(
                    f"Cannot evaluate ELIF statement {self.contents}."
                )


class EvaluableAction(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the Action."""
        first_item = self.contents[0]
        if not isinstance(first_item, Action):
            raise DSLRuntimeError(f"{first_item} is not a valid Action.")
        action: Action = first_item
        action_args = []
        for item in self.contents[1:]:
            if isinstance(item, Operand):
                action_args.append(item.true_value)
            elif isinstance(item, EvaluableList):
                action_args.append(item.evaluate())
            elif isinstance(item, Evaluable):
                action_args.extend(item.evaluate())
        return action.execute(*action_args)


class EvaluableActionArg(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the Action arg."""
        action_args: list[Any] = []
        for item in self.contents:
            if isinstance(item, Operand):
                action_args.append(item.true_value)
            elif isinstance(item, Evaluable):
                action_args.extend(item.evaluate())
        return action_args


class EvaluableList(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the contents of the Evaluable list."""
        list_obj: list[Any] = []
        for item in self.contents:
            if isinstance(item, Operand):
                list_obj.append(item.true_value)
            elif isinstance(item, EvaluableList):
                list_obj.append(item.evaluate())
            elif isinstance(item, Evaluable):
                list_obj.extend(item.evaluate())
        return list_obj


class EvaluableListArg(Evaluable):
    def evaluate(self) -> Any:
        """Evaluate the contents of the Evaluable list arg."""
        list_ext: list[Any] = []
        for item in self.contents:
            if isinstance(item, Operand):
                list_ext.append(item.true_value)
            elif isinstance(item, Evaluable):
                list_ext.extend(item.evaluate())
        return list_ext


class EvaluableExpression(Evaluable):
    def evaluate(self) -> Any:
        """
        Evaluate the contents of the Evaluable expression.

        NOTE: The order of operations is implied by the structure of the grammar
        If the grammar is incorrect, then evaluating the expression will evaluate the
        order of operations incorrectly.
        """
        operators: deque[UnitaryOperator | BinaryOperator] = deque()
        operands: deque[
            Any
        ] = deque()  # Contains the true value of the operands
        for item in self.contents:
            # The only Representable object we care about inside an evaluable expression
            # are the operators, operands, and Evaluable (which we treat as operands).
            if isinstance(item, (UnitaryOperator, BinaryOperator)):
                operators.append(item)
            if isinstance(item, Evaluable):
                operands.append(item.evaluate())
            elif isinstance(item, Operand):
                operands.append(item.true_value)

            if not operators:
                continue

            # Check if there's enough operands to use for the first operator in queue
            if operands and isinstance(operators[0], UnitaryOperator):
                operator = operators.popleft()
                x = operands.pop()
                operands.append(operator.evaluate(x))
            elif len(operands) > 1 and isinstance(
                operators[0], BinaryOperator
            ):
                operator = operators.popleft()
                x, y = operands.popleft(), operands.popleft()
                operands.append(operator.evaluate(x, y))

        if operators:
            raise DSLRuntimeError(
                f"Evaluation of Evaluable has left an unused {operators=}."
            )

        if len(operands) != 1:
            raise DSLRuntimeError(
                f"Evaluation of Evaluable with {self.contents=} did not collapse to "
                "a single value."
            )

        return operands.pop()
