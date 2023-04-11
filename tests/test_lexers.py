from typing import ClassVar

import pytest

from dsl import DefaultLexer
from dsl.models.exceptions import DSLSyntaxError
from dsl.models.symbols import TerminalSymbol
from dsl.models.symbols.terminals import (
    AttributeLiteral,
    ElifLiteral,
    EqualLiteral,
    FloatLiteral,
    GreaterThanLiteral,
    GreaterThanOrEqualLiteral,
    IfLiteral,
    IndexingLiteral,
    IntegerLiteral,
    InvalidSymbol,
    LeftParenthesisLiteral,
    NotEqualLiteral,
    PlusLiteral,
    RightParenthesisLiteral,
    StringLiteral,
    ThenLiteral,
    VariableLiteral,
)


class TestTokenize:
    """Test tokenize."""

    def test_if_statement(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("IF cond THEN output1") == [
            IfLiteral("IF"),
            VariableLiteral("cond"),
            ThenLiteral("THEN"),
            VariableLiteral("output1"),
        ]

    def test_uneven_spaces(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("a+ b  >   c") == [
            VariableLiteral("a"),
            PlusLiteral("+"),
            VariableLiteral("b"),
            GreaterThanLiteral(">"),
            VariableLiteral("c"),
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
            VariableLiteral("a"),
            PlusLiteral("+"),
            VariableLiteral("b"),
            RightParenthesisLiteral(")"),
        ]

    def test_comparison_operators(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("abc == def != ghi >=") == [
            VariableLiteral("abc"),
            EqualLiteral("=="),
            VariableLiteral("def"),
            NotEqualLiteral("!="),
            VariableLiteral("ghi"),
            GreaterThanOrEqualLiteral(">="),
        ]

    def test_attribute_operator(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("abc.cdf == 1") == [
            VariableLiteral("abc"),
            AttributeLiteral(".cdf"),
            EqualLiteral("=="),
            IntegerLiteral("1"),
        ]

    def test_included_symbol(self):
        class FooSymbol(TerminalSymbol):
            regex: ClassVar[str] = "FOOBAR"

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
            VariableLiteral("IF"),
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
        assert lexer.tokenize("'\"£^&(\"(=-ac '") == [
            StringLiteral("'\"£^&(\"(=-ac '")
        ]

    def test_underscore_variable(self):
        lexer = DefaultLexer()
        assert lexer.tokenize("foo_bar") == [VariableLiteral("foo_bar")]


class TestValidateAdjacentTokens:
    """Test validate_adjacent_tokens."""

    def test_valid_tokens(self):
        lexer = DefaultLexer()
        tokens = [
            VariableLiteral("abc"),
            EqualLiteral("=="),
            VariableLiteral("def"),
        ]
        assert lexer.validate_tokens(tokens) is None

    def test_index_and_attribute(self):
        lexer = DefaultLexer()
        tokens = [
            VariableLiteral("abc"),
            IndexingLiteral("[1]"),
            AttributeLiteral(".def"),
        ]
        assert lexer.validate_tokens(tokens) is None

    def test_invalid_token(self):
        lexer = DefaultLexer()
        tokens = [InvalidSymbol("£$@"), VariableLiteral("def")]
        with pytest.raises(DSLSyntaxError):
            assert lexer.validate_tokens(tokens)
