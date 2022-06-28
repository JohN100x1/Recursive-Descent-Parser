from models.symbols import TerminalSymbol


class IfLiteral(TerminalSymbol):
    regex: str = "IF"


class ThenLiteral(TerminalSymbol):
    regex: str = "THEN"


class ElseLiteral(TerminalSymbol):
    regex: str = "ELSE"


class ElifLiteral(TerminalSymbol):
    regex: str = "ELIF"


class ReturnLiteral(TerminalSymbol):
    regex: str = r"RETURN\("


class LeftParenthesisLiteral(TerminalSymbol):
    regex: str = r"\("


class RightParenthesisLiteral(TerminalSymbol):
    regex: str = r"\)"


class CommaLiteral(TerminalSymbol):
    regex: str = ","


class OrLiteral(TerminalSymbol):
    regex: str = "OR"


class AndLiteral(TerminalSymbol):
    regex: str = "AND"


class NotLiteral(TerminalSymbol):
    regex: str = "NOT"


class BoolLiteral(TerminalSymbol):
    regex: str = "TRUE|FALSE"


class EqualLiteral(TerminalSymbol):
    regex: str = "=="


class NotEqualLiteral(TerminalSymbol):
    regex: str = "!="


class GreaterThanLiteral(TerminalSymbol):
    regex: str = ">"


class LessThanLiteral(TerminalSymbol):
    regex: str = "<"


class LessThanOrEqualLiteral(TerminalSymbol):
    regex: str = "<="


class GreaterThanOrEqualLiteral(TerminalSymbol):
    regex: str = ">="


class ModLiteral(TerminalSymbol):
    regex: str = "%"


class MultLiteral(TerminalSymbol):
    regex: str = "*"


class DivLiteral(TerminalSymbol):
    regex: str = "/"


class PlusLiteral(TerminalSymbol):
    regex: str = r"\+"


class MinusLiteral(TerminalSymbol):
    regex: str = "-"


class LeftSquareBracketLiteral(TerminalSymbol):
    regex: str = r"\]"


class RightSquareBracketLiteral(TerminalSymbol):
    regex: str = r"\]"


class NoneLiteral(TerminalSymbol):
    regex: str = "NULL"


class StringLiteral(TerminalSymbol):
    regex: str = "\"[^\"]*\"|'[^']*'"


class FloatLiteral(TerminalSymbol):
    regex: str = r"\d+.\d+"


class IntegerLiteral(TerminalSymbol):
    regex: str = r"\d+"


class VariableSymbol(TerminalSymbol):
    regex: str = r"[A-z_]\w*"


class AttributeSymbol(TerminalSymbol):
    regex: str = r"\.[A-z_]\w*"


class IndexingSymbol(TerminalSymbol):
    regex: str = r"\[\d+\]"


class CountLiteral(TerminalSymbol):
    regex: str = r"COUNT\("


class InvalidSymbol(TerminalSymbol):
    regex: str = r"[^ \n]"
