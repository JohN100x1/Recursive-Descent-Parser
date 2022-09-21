from dsl.models.grammar import Production
from dsl.models.symbols.nonterminals import ExpressionSymbol
from dsl.models.symbols.terminals import IfLiteral


class TestProduction:
    """Test Production."""

    def test_eq(self):
        prod = Production(ExpressionSymbol)
        assert prod != 1
        assert prod == Production(ExpressionSymbol)

    def test_repr(self):
        prod = Production(IfLiteral, ExpressionSymbol)
        assert prod.__repr__() == "Production(IfLiteral, ExpressionSymbol)"
