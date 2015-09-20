from sol.lexer import Token, TokenType
from sol.ast import (
    AstNode,
    ProgramAstNode,
    MsgAstNode,
    IdentAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
    ArgList,
)


class ParseError(Exception):
    pass


class BaseParser:
    def __init__(self, tokens):
        # Stack of tokens (terminals) and AstNodes (nonterminals)
        self.stack = []

        # Tokens remaining in the input program
        self.tokens = tokens

        # TODO - Struct for this
        self.reduce_rules = []

    def parse(self):
        # Shift-reduce until we run out of tokens
        while self.tokens:
            self.shift()
            self.reduce()
        self.reduce()

    def register_reduce_rule(self, expect, reduce_callable):
        self.reduce_rules.append((expect, reduce_callable))

    def shift(self):
        self.stack.append(self.tokens.pop(0))

    def reduce(self):
        while True:
            for expect, reduce_callable in self.reduce_rules:
                tokens = self._cmp_and_pop(expect)
                if not tokens:
                    continue
                ast_node = reduce_callable(*tokens)
                self.stack.append(ast_node)
                break
            else:
                return

    def _cmp_stack_item(self, stack_item, proto):
        """
        Returns True if an item on the stack (either a nonterminal AstNode or
        a terminal Token) matches `proto` (either an AstNode subclass or a
        TokenType value).
        """
        if isinstance(proto, TokenType) and isinstance(stack_item, Token):
            return stack_item.type == proto

        if isinstance(proto, type) and isinstance(stack_item, AstNode):
            return isinstance(stack_item, proto)

        return False

    def _cmp_stack(self, expect):
        """
        Returns True if the top of the stack matches the list `expect`. Each
        item in `expect` is either a subclass of AstNode, or a TokenType
        value.
        """
        if len(self.stack) < len(expect):
            return False

        # Grab the top N items from the stack
        stack_top = self.stack[-len(expect):]

        # Check that each item of the stack matches the expectation
        matches = [self._cmp_stack_item(a, b) for a, b in zip(stack_top, expect)]
        return len(matches) == sum(matches)

    def _cmp_and_pop(self, expect):
        if self._cmp_stack(expect):
            tokens = [self.stack.pop() for x in expect]
            tokens = reversed(tokens)
            return tokens
        return None


class SolParser(BaseParser):
    def __init__(self, *args, **kwargs):
        super(SolParser, self).__init__(*args, **kwargs)

        # MsgAstNode <- x . y
        self.register_reduce_rule(
            [TokenType.IDENT, TokenType.DOT, TokenType.IDENT],
            (lambda target, _, name: MsgAstNode(IdentAstNode(target.value), IdentAstNode(name.value))),
        )

        # MsgAstNode <- MsgAstNode . z
        self.register_reduce_rule(
            [MsgAstNode, TokenType.DOT, TokenType.IDENT],
            (lambda target, _, name: MsgAstNode(target, IdentAstNode(name.value))),
        )

        # AssignAstNode <- x := AstNode
        self.register_reduce_rule(
            [TokenType.IDENT, TokenType.OPER, AstNode],
            (lambda target, _, source: AssignAstNode(IdentAstNode(target.value), source)),
        )

        # ConstAstNode <- "x"
        self.register_reduce_rule(
            [TokenType.STRING],
            (lambda const: ConstAstNode(ConstType.STRING, const.value)),
        )

        # ArgList <- ( AstNode
        self.register_reduce_rule(
            [TokenType.LPAREN, AstNode],
            (lambda _, first_argument: ArgList([first_argument])),
        )

        # ArgList <- ArgList , AstNode
        self.register_reduce_rule(
            [ArgList, TokenType.COMMA, AstNode],
            (lambda existing_arg_list, _, new_argument: ArgList(existing_arg_list.args + [new_argument])),
        )

        # MsgAstNode <- MsgAstNode ArgList )
        self.register_reduce_rule(
            [MsgAstNode, ArgList, TokenType.RPAREN],
            (lambda message_pass, arg_list, _: MsgAstNode(message_pass.target, message_pass.name, arg_list.args)),
        )

        # A Program is made up of either a message pass or an assignment
        self.register_reduce_rule([MsgAstNode, TokenType.EOF], (lambda node, _: ProgramAstNode(node)))
        self.register_reduce_rule([AssignAstNode, TokenType.EOF], (lambda node, _: ProgramAstNode(node)))

    def parse_program(self):
        self.parse()

        if len(self.stack) != 1 or not isinstance(self.stack[0], ProgramAstNode):
            raise ParseError('Unmatched input:', self.stack)
        return self.stack.pop()
