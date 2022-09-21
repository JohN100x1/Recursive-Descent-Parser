from typing import ClassVar

from dsl.models.representables.actions import ReturnAction
from dsl.models.representables.keywords import (
    ElifKeyword,
    ElseKeyword,
    IfKeyword,
    ThenKeyword,
)
from dsl.models.representables.operands import (
    BoolOperand,
    FloatOperand,
    IntegerOperand,
    NoneOperand,
    StringOperand,
    VariableOperand,
)
from dsl.models.representables.operators import (
    AndOperator,
    AttributeOperator,
    CountFunction,
    DivOperator,
    EqualOperator,
    GreaterThanOperator,
    GreaterThanOrEqualOperator,
    IndexingOperator,
    LessThanOperator,
    LessThanOrEqualOperator,
    MinusOperator,
    ModOperator,
    MultOperator,
    NotEqualOperator,
    NotOperator,
    OrOperator,
    PlusOperator,
)
from dsl.models.representables.punctuator import (
    CommaPunctuator,
    LeftParenthesis,
    LeftSquareBracket,
    RightParenthesis,
    RightSquareBracket,
)
from dsl.models.symbols import TerminalSymbol


class IfLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"IF"

    @property
    def represents(self) -> IfKeyword:
        """Return the object the token represents."""
        return IfKeyword()


class ElifLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"ELIF"

    @property
    def represents(self) -> ElifKeyword:
        """Return the object the token represents."""
        return ElifKeyword()


class ThenLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"THEN"

    @property
    def represents(self) -> ThenKeyword:
        """Return the object the token represents."""
        return ThenKeyword()


class ElseLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"ELSE"

    @property
    def represents(self) -> ElseKeyword:
        """Return the object the token represents."""
        return ElseKeyword()


class CountLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"COUNT\("

    @property
    def represents(self) -> CountFunction:
        """Return the object the token represents."""
        return CountFunction(self.lexeme)


class DivLiteral(TerminalSymbol):
    regex: ClassVar[str] = "/"

    @property
    def represents(self) -> DivOperator:
        """Return the object the token represents."""
        return DivOperator(self.lexeme)


class MultLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\*"

    @property
    def represents(self) -> MultOperator:
        """Return the object the token represents."""
        return MultOperator(self.lexeme)


class ModLiteral(TerminalSymbol):
    regex: ClassVar[str] = "%"

    @property
    def represents(self) -> ModOperator:
        """Return the object the token represents."""
        return ModOperator(self.lexeme)


class PlusLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\+"

    @property
    def represents(self) -> PlusOperator:
        """Return the object the token represents."""
        return PlusOperator(self.lexeme)


class MinusLiteral(TerminalSymbol):
    regex: ClassVar[str] = "-"

    @property
    def represents(self) -> MinusOperator:
        """Return the object the token represents."""
        return MinusOperator(self.lexeme)


class GreaterThanOrEqualLiteral(TerminalSymbol):
    regex: ClassVar[str] = ">="

    @property
    def represents(self) -> GreaterThanOrEqualOperator:
        """Return the object the token represents."""
        return GreaterThanOrEqualOperator(self.lexeme)


class LessThanOrEqualLiteral(TerminalSymbol):
    regex: ClassVar[str] = "<="

    @property
    def represents(self) -> LessThanOrEqualOperator:
        """Return the object the token represents."""
        return LessThanOrEqualOperator(self.lexeme)


class LessThanLiteral(TerminalSymbol):
    regex: ClassVar[str] = "<"

    @property
    def represents(self) -> LessThanOperator:
        """Return the object the token represents."""
        return LessThanOperator(self.lexeme)


class GreaterThanLiteral(TerminalSymbol):
    regex: ClassVar[str] = ">"

    @property
    def represents(self) -> GreaterThanOperator:
        """Return the object the token represents."""
        return GreaterThanOperator(self.lexeme)


class EqualLiteral(TerminalSymbol):
    regex: ClassVar[str] = "=="

    @property
    def represents(self) -> EqualOperator:
        """Return the object the token represents."""
        return EqualOperator(self.lexeme)


class NotEqualLiteral(TerminalSymbol):
    regex: ClassVar[str] = "!="

    @property
    def represents(self) -> NotEqualOperator:
        """Return the object the token represents."""
        return NotEqualOperator(self.lexeme)


class NotLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"NOT"

    @property
    def represents(self) -> NotOperator:
        """Return the object the token represents."""
        return NotOperator(self.lexeme)


class AndLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"AND"

    @property
    def represents(self) -> AndOperator:
        """Return the object the token represents."""
        return AndOperator(self.lexeme)


class OrLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"OR"

    @property
    def represents(self) -> OrOperator:
        """Return the object the token represents."""
        return OrOperator(self.lexeme)


class LeftParenthesisLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\("

    @property
    def represents(self) -> LeftParenthesis:
        """Return the object the token represents."""
        return LeftParenthesis()


class RightParenthesisLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\)"

    @property
    def represents(self) -> RightParenthesis:
        """Return the object the token represents."""
        return RightParenthesis()


class NoneLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"None"

    @property
    def represents(self) -> NoneOperand:
        """Return the object the token represents."""
        return NoneOperand(self.lexeme)


class BoolLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"TRUE|FALSE"

    @property
    def represents(self) -> BoolOperand:
        """Return the object the token represents."""
        return BoolOperand(self.lexeme)


class StringLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"'[^']*'|\"[^\"]*\""

    @property
    def represents(self) -> StringOperand:
        """Return the object the token represents."""
        return StringOperand(self.lexeme)


class IndexingLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\[\d+\]"

    @property
    def represents(self) -> IndexingOperator:
        """Return the object the token represents."""
        return IndexingOperator(self.lexeme)


class AttributeLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\.[A-Za-z]\w*"

    @property
    def represents(self) -> AttributeOperator:
        """Return the object the token represents."""
        return AttributeOperator(self.lexeme)


class VariableLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"[A-Za-z]\w*"

    @property
    def represents(self) -> VariableOperand:
        """Return the object the token represents."""
        return VariableOperand(self.lexeme, variables=self.variables)


class FloatLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\d+\.\d+"

    @property
    def represents(self) -> FloatOperand:
        """Return the object the token represents."""
        return FloatOperand(self.lexeme)


class IntegerLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\d+"

    @property
    def represents(self) -> IntegerOperand:
        """Return the object the token represents."""
        return IntegerOperand(self.lexeme)


# This invalid token should be considered last
class InvalidSymbol(TerminalSymbol):
    regex: ClassVar[str] = r"[^ \n]+"

    @property
    def represents(self) -> None:
        """Return the object the token represents."""
        return None


class ReturnLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"RETURN\("

    @property
    def represents(self) -> ReturnAction:
        """Return the object the token represents."""
        return ReturnAction()


class CommaLiteral(TerminalSymbol):
    regex: ClassVar[str] = r","

    @property
    def represents(self) -> CommaPunctuator:
        """Return the object the token represents."""
        return CommaPunctuator()


class LeftSquareBracketLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\["

    @property
    def represents(self) -> LeftSquareBracket:
        """Return the object the token represents."""
        return LeftSquareBracket()


class RightSquareBracketLiteral(TerminalSymbol):
    regex: ClassVar[str] = r"\]"

    @property
    def represents(self) -> RightSquareBracket:
        """Return the object the token represents."""
        return RightSquareBracket()
