from kompressor.lexer import TokenType
from kompressor.ast import MsgAstNode, ConstAstNode


def autoresolve(meth):
    def wrapper(*args, **kwargs):
        return list(meth(*args, **kwargs))
    return wrapper


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0

    @property
    def token(self):
        if self.idx >= len(self.tokens):
            return None
        return self.tokens[self.idx]

    def advance(self):
        token = self.token
        self.idx += 1
        return token

    def expect(self, token_type):
        if not self.peek(token_type):
            raise Exception('Parse error: Unexpected token', self.token.type, token_type)
        return self.advance()

    def peek(self, token_type):
        if self.token is None:
            return False
        return self.token.type == token_type

    def program(self):
        return self.expression()

    def expression(self):
        if self.peek(TokenType.IDENT):
            return self.message_pass()

        return self.const_string()

    def message_pass(self):
        target = self.expect(TokenType.IDENT)
        name = self.expect(TokenType.IDENT)

        args = []
        if self.peek(TokenType.LPAREN):
            args = self.message_arg_list()

        return MsgAstNode(target.value, name.value, args)

    @autoresolve
    def message_arg_list(self):
        self.expect(TokenType.LPAREN)

        while True:
            yield self.expression()
            if not self.peek(TokenType.COMMA):
                break
            self.expect(TokenType.COMMA)

        self.expect(TokenType.RPAREN)

    def const_string(self):
        return ConstAstNode(
            self.expect(TokenType.STRING).value
        )
