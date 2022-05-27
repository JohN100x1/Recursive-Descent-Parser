from typing import Union

from symbols import (
    ExpressionSymbol,
    IntegerLiteral,
    MultLiteral,
    NonTerminalSymbol,
    PlusLiteral,
    TerminalSymbol,
)


class Parser:
    def __init__(self):
        self.parse_tree = {}
        self.tokens = []

    def parse(
        self, tokens: list[TerminalSymbol]
    ) -> dict[str, Union[str, dict]]:
        self.parse_tree = {}
        self.tokens = tokens

        node = ExpressionSymbol()
        self.expand(node, self.parse_tree, 0)

        return self.parse_tree

    def expand(
        self,
        node: NonTerminalSymbol,
        tree: dict[str, Union[str, dict]],
        pointer: int,
    ):
        name = node.name

        i = 1
        while name in tree:
            name = f"{name}_{i}"
            i += 1

        tree[name] = {}
        for production in node.productions:
            print(f"Trying ({name} -> {production.contents()})")
            idx = pointer
            for type_symbol in production.body:
                sym_name = type_symbol.__name__
                print(f"({name} -> {production.contents()}): {sym_name}")
                if idx >= len(self.tokens):
                    print(f"Reject ({name} -> {production.contents()})")
                    tree[name] = {}
                    break

                if issubclass(type_symbol, TerminalSymbol):
                    curr = self.tokens[idx]
                    if isinstance(curr, type_symbol):
                        tree[name][curr.__class__.__name__] = curr.lexeme
                    else:
                        print(f"Reject ({name} -> {production.contents()})")
                        tree[name] = {}
                        break
                else:
                    self.expand(type_symbol(), tree[name], idx)
                idx += 1
            else:
                print(f"Accepted ({name} -> {production.contents()})")
                return
            print("-" * 100)
        del tree[name]


if __name__ == "__main__":
    parser = Parser()
    print(
        parser.parse(
            [
                IntegerLiteral("1"),
                PlusLiteral(),
                IntegerLiteral("2"),
                MultLiteral(),
                IntegerLiteral("3"),
            ]
        )
    )
