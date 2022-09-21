from dsl.models.representables import Representable


class Keyword(Representable):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class IfKeyword(Keyword):
    pass


class ElifKeyword(Keyword):
    pass


class ThenKeyword(Keyword):
    pass


class ElseKeyword(Keyword):
    pass
