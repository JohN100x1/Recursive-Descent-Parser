# Recursive Descent Parser

![Tests](https://github.com/JohN100x1/Recursive-Descent-Parser/actions/workflows/python-workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen)](https://www.python.org/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a recursive descent parser that can handle simple IF statements.
The process has roughly 4 main stages: lexing a string into a list of `TerminalSymbol` objects, parsing this list into a nested tree of `NonterminalSymbol` and `TerminalSymbol` objects, reducing this tree into a `Representable` object tree, and executing this `Representable` tree to return a list of outputs.

Here is the base grammar. Regex definitions for all literals can be found in `terminals.py`.
```bnf
<BlockSymbol> = 
    <IfStatementSymbol> <BlockSymbol>
    | <IfStatementSymbol>

<IfStatementSymbol> = 
    "IF" <ConditionExprSymbol> "THEN" <ActionSymbol> <ElifStatementSymbol>
    | "IF" <ConditionExprSymbol> "THEN" <ActionSymbol>

<ElifStatementSymbol> = 
    "ELSE" <ActionSymbol>
    | "ELIF" <ConditionExprSymbol> "THEN" <ActionSymbol> <ElifStatementSymbol>
    | "ELIF" <ConditionExprSymbol> "THEN" <ActionSymbol>

<ActionSymbol> = 
    "RETURN" <OperandSymbol> RightParenthesisLiteral
    | "RETURN" <OperandSymbol> <ActionArgSymbol>

<ActionArgSymbol> = 
    "," <OperandSymbol> ")"
    | "," <OperandSymbol> <ActionArgSymbol>

<ConditionExprSymbol> = 
    <ConditionTermSymbol> "OR" <ConditionExprSymbol>
    | <ConditionTermSymbol>

<ConditionTermSymbol> = 
    <ConditionFactorSymbol> "AND" <ConditionExprSymbol>
    | <ConditionFactorSymbol>

<ConditionFactorSymbol> = 
    "NOT" <ConditionSymbol>
    | BoolLiteral
    | <ConditionSymbol>

<ConditionSymbol> = 
    <ExpressionSymbol> "==" <ConditionSymbol>
    | <ExpressionSymbol> "!=" <ConditionSymbol>
    | <ExpressionSymbol> ">" <ConditionSymbol>
    | <ExpressionSymbol> "<" <ConditionSymbol>
    | <ExpressionSymbol> "<=" <ConditionSymbol>
    | <ExpressionSymbol> ">=" <ConditionSymbol>
    | <ExpressionSymbol>

<ExpressionSymbol> = 
    <TermSymbol> "+" <ExpressionSymbol>
    | <TermSymbol> "-" <ExpressionSymbol>
    | <TermSymbol>

<TermSymbol> = 
    <FactorSymbol> "*" <ExpressionSymbol>
    | <FactorSymbol> "/" <ExpressionSymbol>
    | <FactorSymbol> "%" <ExpressionSymbol>
    | <FactorSymbol>

<FactorSymbol> = 
    "COUNT(" <ConditionExprSymbol> ")"
    | VariableLiteral AttributeLiteral AttributeLiteral
    | VariableLiteral IndexingLiteral AttributeLiteral
    | VariableLiteral AttributeLiteral
    | VariableLiteral IndexingLiteral
    | <OperandSymbol>
    | "(" <ConditionSymbol> ")"

<OperandSymbol> = 
    VariableLiteral
    | IntegerLiteral
    | FloatLiteral
    | StringLiteral
    | BoolLiteral
    | NoneLiteral
    | <ListSymbol>

<ListSymbol> = 
    "[" <OperandSymbol> "]"
    | "[" <OperandSymbol> <ListArgSymbol>

<ListArgSymbol> = 
    "," <OperandSymbol> "]"
    | "," <OperandSymbol> <ListArgSymbol>
```