from sol.pratt import PrattParser
from sol.lexer import TokenType
from sol.ast import (
    IdentAstNode,
    MsgAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


class SolParser(PrattParser):
    pass


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


SolParser.register_token(
    TokenType.PASS,
    lbp=10,
    nud=None,
    led=led_pass,
)

SolParser.register_token(
    TokenType.ASSIGNMENT,
    lbp=9,
    nud=None,
    led=led_assignment,
)

SolParser.register_token(
    TokenType.IDENT,
    lbp=8,
    nud=(lambda token: IdentAstNode(token.value)),
    led=(lambda parser, left, token: left),
)

SolParser.register_token(
    TokenType.STRING,
    lbp=7,
    nud=(lambda token: ConstAstNode(ConstType.STRING, token.value)),
    led=(lambda parser, left, token: left),
)

SolParser.register_token(
    TokenType.INT,
    lbp=7,
    nud=(lambda token: ConstAstNode(ConstType.INT, token.value)),
    led=(lambda parser, left, token: left),
)

SolParser.register_token(
    TokenType.LPAREN,
    lbp=1,
    nud=None,
    led=led_arg_list,
)

SolParser.register_token(
    TokenType.RPAREN,
    lbp=1,
    nud=None,
    led=(lambda parser, left, token: left),
)
