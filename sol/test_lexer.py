from sol.lexer import Lexer, Token, TokenType


def test_assignment():
    source = 'x := Object.clone'

    lexer = Lexer(source)
    tokens = lexer.iter_match_tokens()
    tokens = list(tokens)

    assert tokens == [
        Token(TokenType.IDENT, 'x'),
        Token(TokenType.OPER, ':='),
        Token(TokenType.IDENT, 'Object'),
        Token(TokenType.DOT, '.'),
        Token(TokenType.IDENT, 'clone'),
    ]


def test_string():
    source = 'x := "Hello world"'

    lexer = Lexer(source)
    tokens = lexer.iter_match_tokens()
    tokens = list(tokens)

    assert tokens == [
        Token(TokenType.IDENT, 'x'),
        Token(TokenType.OPER, ':='),
        Token(TokenType.STRING, 'Hello world'),
    ]


def test_multiple_idents():
    source = 'a bar quux'

    lexer = Lexer(source)
    tokens = lexer.iter_match_tokens()
    tokens = list(tokens)

    assert tokens == [
        Token(TokenType.IDENT, 'a'),
        Token(TokenType.IDENT, 'bar'),
        Token(TokenType.IDENT, 'quux'),
    ]
