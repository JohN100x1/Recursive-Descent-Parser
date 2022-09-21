from quac_core.dsl.models.representables.keywords import IfKeyword


class TestKeyword:
    """Test Keyword."""

    def test_repr(self):
        assert IfKeyword().__repr__() == "IfKeyword()"
