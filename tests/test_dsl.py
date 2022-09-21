from typing import Any

import pytest

from dsl import DefaultDSL, DefaultLexer, DefaultParser, EvaluableAction
from dsl.models import Function
from dsl.models.exceptions import DSLException, DSLSyntaxError, DSLValidationError
from dsl.models.grammar import Grammar, Production, base_grammar
from dsl.models.representables.actions import Action, ReturnAction
from dsl.models.representables.evaluables import (
    EvaluableActionArg,
    EvaluableList,
    EvaluableListArg,
)
from dsl.models.representables.operands import IntegerOperand, NoneOperand
from dsl.models.symbols import TerminalSymbol
from dsl.models.symbols.nonterminals import (
    ActionSymbol,
    ConditionExprSymbol,
    FactorSymbol,
    OperandSymbol,
)
from dsl.models.symbols.terminals import (
    AttributeSymbol,
    BoolLiteral,
    FloatLiteral,
    IndexingSymbol,
    IntegerLiteral,
    NoneLiteral,
    PlusLiteral,
    RightParenthesisLiteral,
    StringLiteral,
    VariableSymbol,
)


class OutcomeAction(Action):
    def validate_args(self, x: Any) -> bool:
        if x not in {1, 2, 3}:
            return False
        return True

    def execute(self, x: Any) -> Any:
        return x


class OutcomeSymbol(TerminalSymbol):
    regex = r"OUTCOME\("

    @property
    def represents(self) -> OutcomeAction:
        return OutcomeAction()


outcome_grammar = Grammar(base_grammar)
outcome_grammar[ActionSymbol] = [
    Production(OutcomeSymbol, VariableSymbol, RightParenthesisLiteral),
    Production(OutcomeSymbol, StringLiteral, RightParenthesisLiteral),
    Production(OutcomeSymbol, IntegerLiteral, RightParenthesisLiteral),
    Production(OutcomeSymbol, FloatLiteral, RightParenthesisLiteral),
    Production(OutcomeSymbol, BoolLiteral, RightParenthesisLiteral),
    Production(OutcomeSymbol, NoneLiteral, RightParenthesisLiteral),
]


class TestDefaultDSLValidate:
    """Test DefaultDSL.validate."""

    @pytest.fixture
    def outcome_dsl(self):
        lexer = DefaultLexer(inclusions=[OutcomeSymbol])
        parser = DefaultParser(grammar=outcome_grammar)
        return DefaultDSL(lexer=lexer, parser=parser)

    def test_null_outcome(self):
        dsl = DefaultDSL()
        input_string = "IF 2 > 1 THEN RETURN(3) ELSE RETURN(None)"
        validation_result = dsl.validate(input_string)
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([ReturnAction(), IntegerOperand("3")]),
            EvaluableAction([ReturnAction(), NoneOperand("None")]),
        ]
        assert validation_result.error is None

    def test_single_outcome(self):
        dsl = DefaultDSL()
        input_string = "IF 2 > 1 THEN RETURN(3)"
        validation_result = dsl.validate(input_string)
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([ReturnAction(), IntegerOperand("3")]),
        ]
        assert validation_result.error is None

    def test_two_outcomes(self):  #
        dsl = DefaultDSL()
        input_string = "IF 1.2 > 3.4 THEN RETURN(5) IF 8 > 6.7 THEN RETURN(9)"
        validation_result = dsl.validate(input_string)
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([ReturnAction(), IntegerOperand("5")]),
            EvaluableAction([ReturnAction(), IntegerOperand("9")]),
        ]
        assert validation_result.error is None

    def test_three_outcomes(self):
        dsl = DefaultDSL()
        input_string = "IF 1.2 > 3.4 THEN RETURN(5) IF 8 > 6.7 THEN RETURN(9) ELSE RETURN(3)"
        validation_result = dsl.validate(input_string)
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([ReturnAction(), IntegerOperand("5")]),
            EvaluableAction([ReturnAction(), IntegerOperand("9")]),
            EvaluableAction([ReturnAction(), IntegerOperand("3")]),
        ]
        assert validation_result.error is None

    @pytest.mark.parametrize(
        "input_stringing",
        [
            "IF 2 £$@ == #~?? 2 THEN RETURN(1)",
            "IF IF THEN RETURN(2)",
            "IF 2 > 1 THEN ELSE",
            "IF 1 == 1 THEN RETURN(3) ELSE RETURN(4) IF",
        ],
    )
    def test_invalid_syntax(self, input_stringing):
        dsl = DefaultDSL()
        validation_result = dsl.validate(input_stringing)
        assert validation_result.is_valid is False
        assert validation_result.actions == []
        assert isinstance(validation_result.error, DSLSyntaxError)

    def test_count_function(self):
        lexer = DefaultLexer(variables={"Answers": ["F1", "F2", "F1", "F1"]})
        dsl = DefaultDSL(lexer=lexer)
        input_string = (
            "IF COUNT(Answers == 'F4') > 0 THEN RETURN(5)"
            "IF COUNT(Answers == 'F3') > 0 THEN RETURN(4)"
            "IF COUNT(Answers == 'F2') > 0 THEN RETURN(3)"
            "IF COUNT(Answers == 'F1') > 0 THEN RETURN(2)"
            "ELSE RETURN(None)"
        )
        validation_result = dsl.validate(input_string)
        assert validation_result.is_valid is True
        assert validation_result.error is None

    def test_included_symbol(self):
        class FooFunction(Function):
            precedence: int = -1
            registrable: bool = True

            def evaluate(self, x: Any) -> Any:
                return x % 3 + 1

        class FooFunc(TerminalSymbol):
            regex: str = r"FooFunc\("

            @property
            def represents(self) -> FooFunction:
                return FooFunction(self.lexeme)

        foo_func_grammar = Grammar(base_grammar)
        foo_func_grammar[FactorSymbol] = [
            Production(FooFunc, ConditionExprSymbol, RightParenthesisLiteral),
            Production(VariableSymbol, AttributeSymbol, AttributeSymbol),
            Production(VariableSymbol, IndexingSymbol, AttributeSymbol),
            Production(VariableSymbol, AttributeSymbol),
            Production(VariableSymbol, IndexingSymbol),
            Production(OperandSymbol),
        ]

        dsl_1 = DefaultDSL()
        validation_result_1 = dsl_1.validate(
            "IF FooFunc(3) == 1 THEN RETURN(3)"
        )
        assert validation_result_1.is_valid is False
        assert validation_result_1.actions == []
        assert isinstance(validation_result_1.error, DSLSyntaxError)

        lexer_2 = DefaultLexer(inclusions=[FooFunc])
        parser_2 = DefaultParser(grammar=foo_func_grammar)
        dsl_2 = DefaultDSL(lexer=lexer_2, parser=parser_2)
        validation_result_2 = dsl_2.validate(
            "IF FooFunc(3) == 1 THEN RETURN(3)"
        )
        assert validation_result_2.is_valid is True
        assert validation_result_2.actions == [
            EvaluableAction([ReturnAction(), IntegerOperand("3")]),
        ]
        assert validation_result_2.error is None

    def test_excluded_symbol(self):
        lexer = DefaultLexer(exclusions=[PlusLiteral])
        dsl = DefaultDSL(lexer=lexer)
        validation_result = dsl.validate("IF 1 + 2 == 3 THEN RETURN(3)")
        assert validation_result.is_valid is False
        assert validation_result.actions == []
        assert isinstance(validation_result.error, DSLException)

    def test_single_action(self, outcome_dsl):
        validation_result = outcome_dsl.validate("IF 2 > 1 THEN OUTCOME(3)")
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([OutcomeAction(), IntegerOperand("3")]),
        ]
        assert validation_result.error is None

        validation_result = outcome_dsl.validate(
            "IF 2 > 1 THEN OUTCOME(2) OUTCOME(3)"
        )
        assert validation_result.is_valid is False
        assert validation_result.actions == []
        assert isinstance(validation_result.error, DSLSyntaxError)

    def test_validate_outcome_valid(self, outcome_dsl):
        validation_result = outcome_dsl.validate("IF 2 > 1 THEN OUTCOME(3)")
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([OutcomeAction(), IntegerOperand("3")]),
        ]
        assert validation_result.error is None

    def test_validate_outcome_invalid(self, outcome_dsl):
        validation_result = outcome_dsl.validate("IF 2 > 1 THEN OUTCOME(4)")
        assert validation_result.is_valid is False
        assert validation_result.actions == []
        assert isinstance(validation_result.error, DSLValidationError)

    def test_validate_outcomes_full(self):
        variables = {
            "Answers": [{"Text": "Pass"}, {"Text": "Fail"}, {"Text": "Pass"}],
            "Score": 0.9,
        }
        lexer = DefaultLexer(inclusions=[OutcomeSymbol], variables=variables)
        parser = DefaultParser(grammar=outcome_grammar)
        dsl = DefaultDSL(lexer=lexer, parser=parser)
        validation_result = dsl.validate(
            "IF COUNT(Answers.Text == 'Fail') > 0 THEN OUTCOME(1)"
            "ELSE OUTCOME(2)"
            "IF Score > 0.85 THEN OUTCOME(3)"
        )
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction([OutcomeAction(), IntegerOperand("1")]),
            EvaluableAction([OutcomeAction(), IntegerOperand("2")]),
            EvaluableAction([OutcomeAction(), IntegerOperand("3")]),
        ]
        assert validation_result.error is None

    def test_validate_multiple_arg_return(self):
        dsl = DefaultDSL()
        validation_result = dsl.validate("IF TRUE THEN RETURN(1,2,3)")
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction(
                [
                    ReturnAction(),
                    IntegerOperand("1"),
                    EvaluableActionArg(
                        [IntegerOperand("2"), IntegerOperand("3")]
                    ),
                ]
            )
        ]
        assert validation_result.error is None

    def test_validate_return_list(self):
        dsl = DefaultDSL()
        validation_result = dsl.validate("IF TRUE THEN RETURN([1,2,3])")
        assert validation_result.is_valid is True
        assert validation_result.actions == [
            EvaluableAction(
                [
                    ReturnAction(),
                    EvaluableList(
                        [
                            IntegerOperand("1"),
                            EvaluableListArg(
                                [IntegerOperand("2"), IntegerOperand("3")]
                            ),
                        ]
                    ),
                ]
            )
        ]
        assert validation_result.error is None

    def test_validate_non_evaluable(self):
        dsl = DefaultDSL(start_symbol=OperandSymbol())
        validation_result = dsl.validate("TRUE")
        assert validation_result.is_valid is False
        assert validation_result.actions == []
        assert isinstance(validation_result.error, DSLValidationError)


class TestDefaultDSLExecute:
    """Test DefaultDSL.execute."""

    class FooObj:
        def __init__(self, bar):
            self.bar = bar

    def test_null_outcome(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF 0 > 1 THEN RETURN(3) ELSE RETURN(None)") == [
            None
        ]

    def test_single_if_statement(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF 2 > 1 THEN RETURN(3)") == [3]

    def test_elif_statement(self):
        dsl = DefaultDSL()
        assert dsl.execute(
            "IF 1 > 2 THEN RETURN(3) ELIF 8 > 6.7 THEN RETURN(9)"
        ) == [9]

    def test_two_if_statement(self):
        dsl = DefaultDSL()
        assert dsl.execute(
            "IF 2 > 1 THEN RETURN(3) IF 3 > 2 THEN RETURN(4)"
        ) == [3, 4]

    def test_else_statement(self):
        input_string = (
            "IF 1 > 2 THEN RETURN(3) IF 4 > 5 THEN RETURN(6) ELSE RETURN(7)"
        )
        dsl = DefaultDSL()
        assert dsl.execute(input_string) == [7]

    def test_parenthesis(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF (1 + 2) == 3 THEN RETURN(3)") == [3]

    def test_nested_parenthesis(self):
        lexer = DefaultLexer(variables={"FooVar": True})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute("IF ((1 + 2) == 3) == FooVar THEN RETURN(3)") == [3]

    def test_not_operator(self):
        dsl = DefaultDSL()
        assert dsl.execute(
            "IF NOT 1 > 2 THEN RETURN('bar') ELSE RETURN(3)"
        ) == ["bar"]

    def test_or_operator(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF 1 > 2 OR 2 > 1 THEN RETURN(3)") == [3]

    def test_and_operator(self):
        input_string = "IF 3 > 2 AND 2 > 3 THEN RETURN(3) ELSE RETURN(None)"
        dsl = DefaultDSL()
        assert dsl.execute(input_string) == [None]

    def test_not_and_or_precedence(self):
        input_string = "IF 0 == 1 OR NOT 2 == 3 AND 4 > 3 THEN RETURN('foo') ELSE RETURN(None)"
        dsl = DefaultDSL()
        assert dsl.execute(input_string) == ["foo"]

    def test_function(self):
        lexer = DefaultLexer(variables={"BooList": [True, False, True]})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute("IF COUNT(BooList) == 2 THEN RETURN(1)") == [1]

    def test_indexing(self):
        input_string = (
            "IF alphabet[2] == 'b' THEN RETURN('b') ELSE RETURN(None)"
        )
        lexer = DefaultLexer(variables={"alphabet": ["a", "b", "c"]})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(input_string) == ["b"]

    def test_attribute(self):
        lexer = DefaultLexer(variables={"foo": self.FooObj(1)})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute("IF foo.bar == 1 THEN RETURN(1)") == [1]

    def test_attribute_list(self):
        variables = {"a": [self.FooObj(1), self.FooObj(2), self.FooObj(3)]}
        lexer = DefaultLexer(variables=variables)
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute("IF COUNT(a.bar == 1) == 1 THEN RETURN(1)") == [1]

    def test_attribute_dict(self):
        lexer = DefaultLexer(variables={"foo": {"bar": 1}})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute("IF foo.bar == 1 THEN RETURN(1)") == [1]

    def test_attribute_dict_stacked_1(self):
        lexer = DefaultLexer(variables={"foo": {"bar": {"cool": 1}}})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(
            "IF foo.bar == 1 THEN RETURN(1) ELSE RETURN(None)"
        ) == [None]

    def test_attribute_dict_stacked_2(self):
        lexer = DefaultLexer(variables={"foo": {"bar": {"cool": 1}}})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(
            "IF foo.bar.cool == 1 THEN RETURN(1) ELSE RETURN(2)"
        ) == [1]

    def test_variable_in_if_statement(self):
        lexer = DefaultLexer(variables={"TotalScore": 0.9, "output": "foobar"})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute("IF TotalScore > 0.8 THEN RETURN(output)") == [
            "foobar"
        ]

    def test_newlines(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF 2 == 2 \n THEN RETURN(1)") == [1]

    def test_invalid_characters(self):
        dsl = DefaultDSL()
        with pytest.raises(DSLSyntaxError):
            assert dsl.execute("IF 2 £$@ == #~?? 2 THEN RETURN(1)") == [1]

    def test_filtering_case_1(self):
        input_string = (
            "IF COUNT(foo.bar == 2) == 2 THEN RETURN(3) ELSE RETURN(None)"
        )
        lexer = DefaultLexer(
            variables={"foo": [{"bar": 1}, {"bar": 2}, {"bar": 2}]}
        )
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(input_string) == [3]

    def test_filtering_case_2(self):
        input_string = "IF COUNT(a.b == 2 AND a.c == 'd') == 1 THEN RETURN(3) ELSE RETURN(None)"
        variables = {
            "a": [{"b": 1, "c": "d"}, {"b": 2, "c": "d"}, {"b": 2, "c": "e"}]
        }
        lexer = DefaultLexer(variables=variables)
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(input_string) == [3]

    def test_filtering_case_3(self):
        input_string = (
            "IF COUNT(a.b == 2 AND NOT a.c == 'd') == 1 "
            "THEN RETURN(3) ELSE RETURN(None)"
        )
        variables = {
            "a": [{"b": 3, "c": "d"}, {"b": 2, "c": "d"}, {"b": 2, "c": "e"}]
        }
        lexer = DefaultLexer(variables=variables)
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(input_string) == [3]

    def test_count_function_f2(self):
        input_string = (
            "IF COUNT(Answers == 'F4') > 0 THEN RETURN(4)"
            "IF COUNT(Answers == 'F3') > 0 THEN RETURN(3)"
            "IF COUNT(Answers == 'F2') > 0 THEN RETURN(2)"
            "IF COUNT(Answers == 'F1') > 0 THEN RETURN(1)"
            "ELSE RETURN(None)"
        )
        lexer = DefaultLexer(variables={"Answers": ["F1", "F2", "F1", "F1"]})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(input_string) == [2, 1]

    def test_count_function_none(self):
        input_string = (
            "IF COUNT(Answers == 'F4') > 0 THEN RETURN(4)"
            "IF COUNT(Answers == 'F3') > 0 THEN RETURN(3)"
            "IF COUNT(Answers == 'F2') > 0 THEN RETURN(2)"
            "IF COUNT(Answers == 'F1') > 0 THEN RETURN(1)"
            "ELSE RETURN(None)"
        )
        lexer = DefaultLexer(variables={"Answers": ["F0", "F0", "F0", "F0"]})
        dsl = DefaultDSL(lexer=lexer)
        assert dsl.execute(input_string) == [None]

    def test_count_nested_action(self):
        dsl = DefaultDSL()
        with pytest.raises(DSLSyntaxError, match="Input cannot be parsed."):
            assert dsl.execute("IF 3 > 2 THEN RETURN(RETURN(3))")

    def test_count_sequential_actions(self):
        dsl = DefaultDSL()
        with pytest.raises(DSLSyntaxError, match="Input cannot be parsed."):
            assert dsl.execute("IF 3 > 2 THEN RETURN(1) RETURN(2)") == [1, 2]

    def test_outcomes_full(self):
        variables = {
            "Answers": [{"Text": "Pass"}, {"Text": "Fail"}],
            "Score": 0.9,
        }
        lexer = DefaultLexer(inclusions=[OutcomeSymbol], variables=variables)
        parser = DefaultParser(grammar=outcome_grammar)
        dsl = DefaultDSL(lexer=lexer, parser=parser)
        assert dsl.execute(
            "IF COUNT(Answers.Text == 'Fail') > 0 THEN OUTCOME(1)"
            "ELSE OUTCOME(2)"
            "IF Score > 0.85 THEN OUTCOME(3)"
        ) == [1, 3]

    def test_function_as_factor(self):
        variables = {
            "Answers": [
                {"Text": "Pass", "OptionNumId": 1},
                {"Text": "Fail", "OptionNumId": 2},
                {"Text": "Fail", "OptionNumId": 1},
            ],
        }
        lexer = DefaultLexer(inclusions=[OutcomeSymbol], variables=variables)
        parser = DefaultParser(grammar=outcome_grammar)
        dsl = DefaultDSL(lexer=lexer, parser=parser)

        input_string = (
            "IF COUNT(Answers.Text == 'Fail') / 3 > 0.2 THEN OUTCOME(3)"
        )
        assert dsl.execute(input_string) == [3]

    def test_multiple_arg_return(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF TRUE THEN RETURN(1,2,3)") == [(1, 2, 3)]

    def test_return_list(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF TRUE THEN RETURN([1,2,3])") == [[1, 2, 3]]

    def test_two_lists(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF COUNT([1,0,1]) == 2 THEN RETURN([1,2,3])") == [
            [1, 2, 3]
        ]

    def test_nested_lists(self):
        dsl = DefaultDSL()
        assert dsl.execute("IF TRUE THEN RETURN([[1,2],2,3])") == [
            [[1, 2], 2, 3]
        ]
