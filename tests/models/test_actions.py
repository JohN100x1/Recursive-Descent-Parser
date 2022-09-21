from quac_core.dsl.models.representables.actions import ReturnAction


class TestAction:
    """Test Action class."""

    def test_repr(self):
        assert ReturnAction().__repr__() == "ReturnAction()"

    def test_not_eq(self):
        assert ReturnAction() != "foobar"
