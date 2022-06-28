import logging
from collections import deque
from typing import MutableSequence, Optional, Type

from models.exceptions import DSLSyntaxError
from models.grammar import Grammar, Production, base_grammar
from models.symbols import NonTerminalSymbol, TerminalSymbol, TSymbol
from models.symbols.nonterminals import BlockSymbol

logger = logging.getLogger(__name__)


class Parser:
    DEFAULT_START_SYMBOL: Type[NonTerminalSymbol] = BlockSymbol

    def __init__(self, grammar: Optional[Grammar] = None):
        self.grammar = grammar or base_grammar
        self.parse_tree: MutableSequence[TSymbol] = deque()
        self.tokens: list[TerminalSymbol] = []
        self.terminals: list[TerminalSymbol] = []

        self.rejected: set[tuple[Production, int]] = set()

    def parse(
        self,
        tokens: list[TerminalSymbol],
        start_symbol: Optional[NonTerminalSymbol] = None,
    ) -> list[TSymbol]:
        """
        Parse a list of terminals from a starting non-terminal.
        :param tokens: A list of terminals.
        :param start_symbol: A optional non-terminal.
        :return: A parse tree represented by a list of nested tokens.
        """
        self.parse_tree = deque()
        self.tokens = tokens
        self.rejected = set()

        node = start_symbol or self.DEFAULT_START_SYMBOL()
        pointer = self.expand(node, self.parse_tree, 0)
        logger.debug(f"Parse Tree: {self.parse_tree}")
        if not self.parse_tree or pointer < len(self.tokens):
            raise DSLSyntaxError("Input cannot be parsed.")
        return list(self.parse_tree)

    def expand(
        self,
        node: NonTerminalSymbol,
        tree: MutableSequence[TSymbol],
        origin: int,
    ) -> int:
        """
        Expand a parse tree by trying all possible productions in the subtree.
        :param node: The non-terminal node to expand.
        :param tree: The super-tree of the non-terminal node.
        :param origin: Starting index of terminal list to predict production.
        :return: The total number of terminals contained within expanded tree.
        """
        tree.append(node)
        for production in self.grammar[node.__class__]:

            if (production, origin) in self.rejected:
                continue
            pointer = origin
            for symbol_type in production.body:
                if pointer >= len(self.tokens):
                    break

                if issubclass(symbol_type, TerminalSymbol):
                    curr = self.tokens[pointer]
                    if isinstance(curr, symbol_type):
                        node.contents.append(curr)
                        pointer += 1
                        continue
                    else:
                        break

                terminal_count = self.expand(
                    symbol_type(), node.contents, pointer
                )
                if terminal_count == 0:
                    break
                pointer += terminal_count
            else:
                return pointer - origin
            node.contents = deque()
            self.rejected.add((production, origin))
        tree.pop()
        return 0
