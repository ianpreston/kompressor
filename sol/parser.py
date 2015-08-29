from sol.lexer import TokenType
from sol.ast import (
    MsgAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


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
        return self.expr()

    def expr(self):
        if self.peek(TokenType.IDENT):
            left_token = self.expect(TokenType.IDENT)

            if self.peek(TokenType.IDENT):
                return self.expr_message_pass(left_token)
            else:
                return self.expr_assignment(left_token)

        else:
            return self.expr_const()

    def expr_message_pass(self, target):
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

    def expr_assignment(self, ident):
        self.expect(TokenType.ASSIGNMENT)
        value = self.expr()

        return AssignAstNode(
            ConstAstNode(ConstType.STRING, ident.value),
            value,
        )

    def expr_const(self):
        if self.peek(TokenType.STRING):
            return self.const_string()
        else:
            return self.const_int()

    def const_string(self):
        return ConstAstNode(
            ConstType.STRING,
            self.expect(TokenType.STRING).value,
        )

    def const_int(self):
        return ConstAstNode(
            ConstType.INT,
            int(self.expect(TokenType.INT).value),
        )
