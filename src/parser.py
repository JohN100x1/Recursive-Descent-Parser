import logging

from symbols import (
    ExpressionSymbol,
    IntegerLiteral,
    MultLiteral,
    NonTerminalSymbol,
    PlusLiteral,
    TerminalSymbol,
    TSymbol,
)

logger = logging.getLogger(__name__)


class Parser:
    def __init__(self):
        self.parse_tree = {}
        self.tokens = []

    def parse(self, tokens: list[TerminalSymbol]) -> list[TSymbol]:
        self.parse_tree = []
        self.tokens = tokens

        node = ExpressionSymbol()
        self.expand(node, self.parse_tree, 0)
        logger.info(f"Parse Tree: {self.parse_tree}")

        return self.parse_tree

    def expand(
        self, node: NonTerminalSymbol, tree: list[TSymbol], pivot: int
    ) -> int:
        tree.append(node)
        for production in node.productions:
            prod = f"({node} -> {production.symbols()})"
            logger.info(f"Trying {prod}")
            pointer = pivot
            for i, symbol_type in enumerate(production.body, 1):
                symbol_name = symbol_type.__name__
                logger.info(f"{i}. {prod}: {symbol_name}")
                if pointer >= len(self.tokens):
                    logger.info(
                        f"Rejected {prod}: "
                        f"Cannot fit production to {self.tokens[pivot:]}"
                    )
                    node.contents = []
                    break

                if issubclass(symbol_type, TerminalSymbol):
                    curr = self.tokens[pointer]
                    if isinstance(curr, symbol_type):
                        node.contents.append(curr)
                        pointer += 1
                    else:
                        logger.info(
                            f"Rejected {prod}: {curr} is not a {symbol_name}"
                        )
                        node.contents = []
                        break
                else:
                    terminal_count = self.expand(
                        symbol_type(), node.contents, pointer
                    )
                    pointer += terminal_count
            else:
                logger.info(f"Accepted {prod}")
                return pointer - pivot
            logger.info("-" * 100)
        tree.pop()
        return 0


if __name__ == "__main__":
    parser = Parser()
    parse_tree = parser.parse(
        [
            IntegerLiteral("1"),
            MultLiteral(),
            IntegerLiteral("2"),
            PlusLiteral(),
            IntegerLiteral("3"),
        ]
    )
    print(parse_tree)
