import pytest

from dsl.models import Punctuator
from dsl.models.representables.punctuator import LeftParenthesis


class TestPunctuator:
    """Test Punctuator."""

    def test_repr(self):
        assert LeftParenthesis().__repr__() == "LeftParenthesis()"

    def test_eq(self):
        assert LeftParenthesis() == LeftParenthesis()
        assert LeftParenthesis() != "foo"

    def test_no_precedence(self):
        with pytest.raises(AttributeError, match="precedence"):

            class Bar(Punctuator):
                pass

            assert Bar()
