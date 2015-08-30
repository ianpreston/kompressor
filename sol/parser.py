from sol.lexer import TokenType
from sol.ast import (
    IdentAstNode,
    MsgAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


class Parser:
    lbp_map = {}
    nud_map = {}
    led_map = {}

    @classmethod
    def register_token(cls, token_type, lbp, nud, led):
        cls.lbp_map[token_type] = lbp
        cls.nud_map[token_type] = nud
        cls.led_map[token_type] = led

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

    def expr(self, rbp=0):
        left = self.nud(self.token)
        while rbp < self.lbp(self.token):
            self.advance()
            if not self.token:
                return left
            left = self.led(left, self.last_token)
        return left

    def nud(self, token):
        cable = self.nud_map.get(token.type)
        if not cable:
            raise Exception('Unexpected token', token)
        return cable(token)

    def led(self, left, token):
        cable = self.led_map.get(token.type)
        if not cable:
            raise Exception('Unexpected token', token)
        return cable(self, left, token)

    def lbp(self, token):
        return self.lbp_map.get(token.type, 1)


def led_pass(parser, left, token):
    expr = parser.expr(parser.lbp(token))
    return MsgAstNode(
        target=left,
        name=expr,
        args=None,
    )


def led_arg_list(parser, left, token):
    args = []

    while True:
        expr = parser.expr(parser.lbp(token))
        args.append(expr)

        if parser.token.type == TokenType.RPAREN:
            break

        if parser.token.type == TokenType.COMMA:
            parser.advance()
            continue

        raise Exception('Invalid token in led_arg_list()', parser.token)

    left.args = args
    return left


def led_assignment(parser, left, token):
    expr = parser.expr(parser.lbp(token))
    return AssignAstNode(left, expr)

Parser.register_token(
    TokenType.PASS,
    lbp=10,
    nud=None,
    led=led_pass,
)

Parser.register_token(
    TokenType.ASSIGNMENT,
    lbp=9,
    nud=None,
    led=led_assignment,
)

Parser.register_token(
    TokenType.IDENT,
    lbp=8,
    nud=(lambda token: IdentAstNode(token.value)),
    led=(lambda parser, left, token: left),
)

Parser.register_token(
    TokenType.STRING,
    lbp=7,
    nud=(lambda token: ConstAstNode(ConstType.STRING, token.value)),
    led=(lambda parser, left, token: left),
)

Parser.register_token(
    TokenType.INT,
    lbp=7,
    nud=(lambda token: ConstAstNode(ConstType.INT, token.value)),
    led=(lambda parser, left, token: left),
)

Parser.register_token(
    TokenType.LPAREN,
    lbp=1,
    nud=None,
    led=led_arg_list,
)

Parser.register_token(
    TokenType.RPAREN,
    lbp=1,
    nud=None,
    led=(lambda parser, left, token: left),
)
