import pytest

from quac_core.dsl import DefaultLexer
from quac_core.dsl.models.exceptions import DSLSyntaxError
from quac_core.dsl.models.symbols import TerminalSymbol
from quac_core.dsl.models.symbols.terminals import (
    AttributeSymbol,
    ElifLiteral,
    EqualLiteral,
    FloatLiteral,
    GreaterThanLiteral,
    GreaterThanOrEqualLiteral,
    IfLiteral,
    IndexingSymbol,
    IntegerLiteral,
    InvalidSymbol,
    LeftParenthesisLiteral,
    NotEqualLiteral,
    PlusLiteral,
    RightParenthesisLiteral,
    StringLiteral,
    ThenLiteral,
    VariableSymbol,
)


class TestTokenize:
    """Test tokenize."""

    def test_if_statement(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("IF cond THEN output1") == [
            IfLiteral("IF"),
            VariableSymbol("cond"),
            ThenLiteral("THEN"),
            VariableSymbol("output1"),
        ]

    def test_uneven_spaces(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("a+ b  >   c") == [
            VariableSymbol("a"),
            PlusLiteral("+"),
            VariableSymbol("b"),
            GreaterThanLiteral(">"),
            VariableSymbol("c"),
        ]

    def test_numbers(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("1 + 2.3") == [
            IntegerLiteral("1"),
            PlusLiteral("+"),
            FloatLiteral("2.3"),
        ]

    def test_parenthesis(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("(a+b)") == [
            LeftParenthesisLiteral("("),
            VariableSymbol("a"),
            PlusLiteral("+"),
            VariableSymbol("b"),
            RightParenthesisLiteral(")"),
        ]

    def test_comparison_operators(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("abc == def != ghi >=") == [
            VariableSymbol("abc"),
            EqualLiteral("=="),
            VariableSymbol("def"),
            NotEqualLiteral("!="),
            VariableSymbol("ghi"),
            GreaterThanOrEqualLiteral(">="),
        ]

    def test_attribute_operator(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("abc.cdf == 1") == [
            VariableSymbol("abc"),
            AttributeSymbol(".cdf"),
            EqualLiteral("=="),
            IntegerLiteral("1"),
        ]

    def test_included_symbol(self):
        class FooSymbol(TerminalSymbol):
            regex: str = "FOOBAR"

            def represents(self) -> None:
                return None

        lexer = DefaultLexer(inclusions=[FooSymbol])
        assert lexer.tokenize("FOOBAR == 3") == [
            FooSymbol("FOOBAR"),
            EqualLiteral("=="),
            IntegerLiteral("3"),
        ]

    def test_excluded_symbol(self):
        lexer = DefaultLexer(exclusions=[IfLiteral])
        assert lexer.tokenize("IF == 3") == [
            VariableSymbol("IF"),
            EqualLiteral("=="),
            IntegerLiteral("3"),
        ]

    def test_elif(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("ELIF") == [ElifLiteral("ELIF")]

    def test_string_with_spaces(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("'Hey there'") == [StringLiteral("'Hey there'")]

    def test_string_with_underscore(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("'Hey_there'") == [StringLiteral("'Hey_there'")]

    def test_single_string_with_random_stuff_inside(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("'\"£^&(\"(=-ac '") == [StringLiteral("'\"£^&(\"(=-ac '")]

    def test_underscore_variable(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("foo_bar") == [VariableSymbol("foo_bar")]


class TestValidateAdjacentTokens:
    """Test validate_adjacent_tokens."""

    def test_valid_tokens(self):
        lexer = DefaultLexer()
        tokens = [VariableSymbol("abc"), EqualLiteral("=="), VariableSymbol("def")]
        assert lexer.validate_tokens(tokens) is None

    def test_index_and_attribute(self):
        lexer = DefaultLexer()
        tokens = [VariableSymbol("abc"), IndexingSymbol("[1]"), AttributeSymbol(".def")]
        assert lexer.validate_tokens(tokens) is None

    def test_invalid_token(self):
        lexer = DefaultLexer()
        tokens = [InvalidSymbol("£$@"), VariableSymbol("def")]
        with pytest.raises(DSLSyntaxError):
            assert lexer.validate_tokens(tokens)
