import pytest
from sol.parser import SolParser, ParseError
from sol.lexer import Token, TokenType
from sol.ast import (
    MsgAstNode,
    IdentAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


def test_msg_pass():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'bar'),
    ]

    parser = SolParser(tokens)
    root = parser.parse_program().root

    assert isinstance(root, MsgAstNode)
    assert root.target.ident == 'foo'
    assert root.name.ident == 'bar'
    assert not root.args


def test_invalid_msg_pass():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.IDENT, 'bar'),
    ]

    parser = SolParser(tokens)

    with pytest.raises(ParseError):
        parser.parse_program()


def test_nonsense():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.STRING, 'hello world'),
    ]

    parser = SolParser(tokens)

    with pytest.raises(ParseError):
        parser.parse_program()


def test_assignment():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.OPER, ':='),
        Token(TokenType.IDENT, 'bar'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'quux'),
    ]

    parser = SolParser(tokens)
    root = parser.parse_program().root

    assert isinstance(root, AssignAstNode)

    assert isinstance(root.left, IdentAstNode)
    assert root.left.ident == 'foo'

    assert isinstance(root.right, MsgAstNode)
    assert root.right.target.ident == 'bar'
    assert root.right.name.ident == 'quux'


def test_assignment_string():
    tokens = [
        Token(TokenType.IDENT, 'str'),
        Token(TokenType.OPER, ':='),
        Token(TokenType.STRING, 'Hello, world!'),
    ]

    parser = SolParser(tokens)
    root = parser.parse_program().root

    assert isinstance(root, AssignAstNode)

    assert isinstance(root.left, IdentAstNode)
    assert root.left.ident == 'str'

    assert isinstance(root.right, ConstAstNode)
    assert root.right.const_type == ConstType.STRING
    assert root.right.const_value == 'Hello, world!'


def test_argument():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'bar'),
        Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'the_target'),
            Token(TokenType.DOT, '.'),
            Token(TokenType.IDENT, 'the_name'),
        Token(TokenType.RPAREN, ')'),
    ]

    parser = SolParser(tokens)
    root = parser.parse_program().root

    assert isinstance(root, MsgAstNode)
    assert root.target.ident == 'foo'
    assert root.name.ident == 'bar'

    assert len(root.args) == 1
    assert isinstance(root.args[0], MsgAstNode)
    assert root.args[0].target.ident == 'the_target'
    assert root.args[0].name.ident == 'the_name'


def test_incomplete_arguments():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'bar'),
        Token(TokenType.LPAREN, '('),
        Token(TokenType.IDENT, 'the_target'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'the_name'),
    ]

    parser = SolParser(tokens)
    with pytest.raises(ParseError):
        parser.parse_program()


def test_multiple_const_arguments():
    tokens = [
        Token(TokenType.IDENT, 'foo'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'bar'),
        Token(TokenType.LPAREN, '('),
            Token(TokenType.STRING, 'first argument'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.STRING, 'second argument'),
        Token(TokenType.RPAREN, ')'),
    ]

    parser = SolParser(tokens)
    root = parser.parse_program().root

    assert isinstance(root, MsgAstNode)
    assert root.target.ident == 'foo'
    assert root.name.ident == 'bar'
    assert len(root.args) == 2

    assert isinstance(root.args[0], ConstAstNode)
    assert isinstance(root.args[1], ConstAstNode)

    assert root.args[0].const_value == 'first argument'
    assert root.args[1].const_value == 'second argument'
