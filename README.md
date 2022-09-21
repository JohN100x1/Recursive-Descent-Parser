# Recursive Descent Parser

![Tests](https://github.com/JohN100x1/Recursive-Descent-Parser/actions/workflows/python-workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen)](https://www.python.org/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a recursive descent parser that can handle simple IF statements.
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
    | <VariableSymbol> <AttributeSymbol> <AttributeSymbol>
    | <VariableSymbol> <IndexingSymbol> <AttributeSymbol>
    | <VariableSymbol> <AttributeSymbol>
    | <VariableSymbol> <IndexingSymbol>
    | <OperandSymbol>
    | "(" <ConditionSymbol> ")"

<OperandSymbol> = 
    <VariableSymbol>
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