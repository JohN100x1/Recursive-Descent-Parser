import pytest

from quac_core.dsl.models.symbols import NonTerminalSymbol, TerminalSymbol
from quac_core.dsl.models.symbols.nonterminals import ExpressionSymbol
from quac_core.dsl.models.symbols.terminals import IntegerLiteral, InvalidSymbol


class TestTerminalSymbol:
    """Test TerminalSymbol."""

    def test_no_regex(self):
        with pytest.raises(AttributeError, match="regex"):

            class Foo(TerminalSymbol):
                def represents(self):
                    return None

            assert Foo("1")

    def test_not_eq(self):
        assert IntegerLiteral("2") != 3

    def test_invalid_token_represents_none(self):
        assert InvalidSymbol("£$@").represents is None


class TestNonTerminalSymbol:
    """Test NonterminalSymbol."""

    def test_no_represents(self):
        with pytest.raises(AttributeError, match="represents"):

            class Bar(NonTerminalSymbol):
                pass

            assert Bar()

    def test_not_eq(self):
        assert ExpressionSymbol([]) != 1
