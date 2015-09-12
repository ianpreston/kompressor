from sol.lexer import Token, TokenType
from sol.ast import (
    AstNode,
    MsgAstNode,
    IdentAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


class ShiftReduceParser:
    def __init__(self, tokens):
        # Stack of tokens (terminals) and AstNodes (nonterminals)
        self.stack = []

        # Tokens remaining in the input program
        self.tokens = tokens

        # TODO - Struct for this
        self.reduce_rules = []

    def program(self):
        while self.tokens:
            self.shift()
            self.reduce()

        last_stack = None
        while last_stack != self.stack:
            last_stack = self.stack
            self.reduce()

        # TODO - Need a reduce rule for a root AST node
        return self.stack[0]

    def register_reduce_rule(self, expect, reduce_callable):
        self.reduce_rules.append((expect, reduce_callable))

    def shift(self):
        self.stack.append(self.tokens.pop(0))

    def reduce(self):
        for expect, reduce_callable in self.reduce_rules:
            tokens = self._cmp_and_pop(expect)
            if not tokens:
                continue
            ast_node = reduce_callable(*tokens)
            self.stack.append(ast_node)
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


class SolParser(ShiftReduceParser):
    def __init__(self, *args, **kwargs):
        super(SolParser, self).__init__(*args, **kwargs)

        # x.y
        self.register_reduce_rule(
            [TokenType.IDENT, TokenType.DOT, TokenType.IDENT],
            (lambda target, _, name: MsgAstNode(IdentAstNode(target.value), IdentAstNode(name.value))),
        )

        # x.y.z
        self.register_reduce_rule(
            [MsgAstNode, TokenType.DOT, TokenType.IDENT],
            (lambda target, _, name: MsgAstNode(target, IdentAstNode(name.value))),
        )

        # x := y.z
        self.register_reduce_rule(
            [TokenType.IDENT, TokenType.OPER, AstNode],
            (lambda target, _, source: AssignAstNode(IdentAstNode(target.value), source)),
        )

        # "x"
        self.register_reduce_rule(
            [TokenType.STRING],
            (lambda const: ConstAstNode(ConstType.STRING, const.value)),
        )

        # (x.y, foo.bar)
        self.register_reduce_rule(
            [TokenType.RPAREN],
            self.parse_arg_list,
        )

    def parse_arg_list(self, rparen):
        arguments = []

        # Walk down the stack from top to bottom, removing items until we
        # reach a left paren
        while True:
            item = self.stack.pop()

            if self._cmp_stack_item(item, TokenType.LPAREN):
                break

            if self._cmp_stack_item(item, TokenType.COMMA):
                continue

            if self._cmp_stack_item(item, AstNode):
                arguments.insert(0, item)
                continue

            # TODO - Enforce commas between AstNodes

            raise Exception('Unexpected stack item', item)

        # After finding the left paren, expect a MsgAstNode (the message pass for
        # which we are parsing arguments)
        ast_node, = self._cmp_and_pop([MsgAstNode])

        # Assign the parsed argument list to this MsgAstNode, and return it
        # as the result of this reduction.
        ast_node.args = arguments
        return ast_node
