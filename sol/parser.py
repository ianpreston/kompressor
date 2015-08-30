from sol.lexer import TokenType
from sol.ast import (
    IdentAstNode,
    MsgAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0

    @property
    def token(self):
        if self.idx >= len(self.tokens):
            return None
        return self.tokens[self.idx]

    @property
    def last_token(self):
        return self.tokens[self.idx-1]

    def advance(self):
        self.idx += 1

    def program(self):
        return self.expr()

    def nud(self, token):
        if token.type == TokenType.IDENT:
            return IdentAstNode(token.value)

        if token.type == TokenType.STRING:
            return ConstAstNode(ConstType.STRING, token.value)

        if token.type == TokenType.INT:
            return ConstAstNode(ConstType.INT, int(token.value))

        if token.type == TokenType.SEMICOLON:
            return 'EOF'

        raise Exception('Invalid token for nud()', token)

    def led(self, left, token):
        # TODO - Registrar/map

        if token.type in (
            TokenType.IDENT,
            TokenType.STRING,
            TokenType.INT,
            TokenType.SEMICOLON,
        ):
            return left

        if token.type == TokenType.PASS:
            expr = self.expr(self.lbp(token))
            return MsgAstNode(
                target=left,
                name=expr,
                args=None,
            )

        if token.type == TokenType.ASSIGNMENT:
            expr = self.expr(self.lbp(token))
            return AssignAstNode(left, expr)

        if token.type == TokenType.LPAREN:
            return self.led_arg_list(left, token)

        if token.type == TokenType.RPAREN:
            return left

        raise Exception('Invalid token for led()', token)

    def lbp(self, token):
        # TODO - Registrar/map

        if token.type == TokenType.PASS:
            return 10
        if token.type == TokenType.ASSIGNMENT:
            return 9
        if token.type == TokenType.IDENT:
            return 8
        if token.type in (TokenType.STRING, TokenType.INT):
            return 7
        if token.type == TokenType.SEMICOLON:
            return 0
        return 1

    def expr(self, rbp=0):
        left = self.nud(self.token)
        while rbp < self.lbp(self.token):
            self.advance()
            if not self.token:
                return left
            left = self.led(left, self.last_token)
        return left

    def led_arg_list(self, left, token):
        args = []

        while True:
            expr = self.expr(self.lbp(token))
            args.append(expr)

            if self.token.type == TokenType.RPAREN:
                break

            if self.token.type == TokenType.COMMA:
                self.advance()
                continue

            raise Exception('Invalid token in led_arg_list()', self.token)

        left.args = args
        return left
