import logging
from abc import ABC, abstractmethod
from collections import deque
from typing import ClassVar, MutableSequence, Type

from dsl.models import Grammar, Punctuator
from dsl.models.exceptions import DSLSyntaxError
from dsl.models.grammar import Production, base_grammar
from dsl.models.representables import Representable
from dsl.models.symbols import NonTerminalSymbol, TerminalSymbol, TSymbol
from dsl.models.symbols.nonterminals import BlockSymbol

logger = logging.getLogger(__name__)


class Parser(ABC):
    DEFAULT_START_SYMBOL: ClassVar[Type[NonTerminalSymbol]]

    @abstractmethod
    def parse(
        self,
        tokens: list[TerminalSymbol],
        start_symbol: NonTerminalSymbol | None = None,
    ) -> list[TSymbol]:
        """Parse a list of terminals from a starting non-terminal."""
        ...

    @abstractmethod
    def reduce(self, node: TSymbol) -> list[Representable]:
        """
        Reduce a parse tree into an abstract syntax tree of objects
        the symbols represent.
        """
        ...


class DefaultParser(Parser):
    DEFAULT_START_SYMBOL: ClassVar[Type[NonTerminalSymbol]] = BlockSymbol

    def __init__(self, grammar: Grammar | None = None):
        self.grammar = grammar or base_grammar
        self.parse_tree: MutableSequence[TSymbol] = deque()
        self.tokens: list[TerminalSymbol] = []
        self.terminals: list[TerminalSymbol] = []

        self.rejected: set[tuple[Production, int]] = set()

    def parse(
        self,
        tokens: list[TerminalSymbol],
        start_symbol: NonTerminalSymbol | None = None,
    ) -> list[TSymbol]:
        """
        Parse a list of terminals from a starting non-terminal.
        :param tokens: A list of terminals
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
        Expand a parse tree by trying all possible productions in the subtree
        :param node: The non-terminal node to expand
        :param tree: The super-tree of the non-terminal node.
        :param origin: The starting index of the terminal list to try to fit production.
        :return: The total number of terminals contained within the expanded tree.
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

    def reduce(self, node: TSymbol) -> list[Representable]:
        """
        Reduces the parse tree into an execution tree
        :param node: A terminal or non-terminal symbol.
        :return: A list of Representable objects (i.e. objects a symbol represents).
        """
        if isinstance(node, TerminalSymbol):
            return [node.represents]

        non_punctuations = [
            sub_node
            for sub_node in node.contents
            if not isinstance(sub_node.represents, Punctuator)
        ]

        if len(non_punctuations) > 1 or isinstance(node, BlockSymbol):
            non_terminal_represent = node.represents()
            for sub_node in non_punctuations:
                non_terminal_represent.contents.extend(self.reduce(sub_node))
            return [non_terminal_represent]
        return self.reduce(non_punctuations[0])
