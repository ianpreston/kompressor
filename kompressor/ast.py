from kompressor.io import IoState, IoMessage


class Interpreter:
    def __init__(self):
        pass

    def evaluate_ast_node(self, node):
        if isinstance(node, str):
            return IoState.resolve_name(node)

        if isinstance(node, ConstAstNode):
            return node.const_value

        sender = IoState.current_context()
        target = self.evaluate_ast_node(node.target)

        # Recursively evaluate this node's arguments, which are themselves
        # message pass expressions
        resolved_args = [self.evaluate_ast_node(arg) for arg in node.args]

        message = IoMessage(sender, target, node.name, resolved_args)
        return IoState.evaluate(message)


class AstNode:
    """
    AstNode represents a parsed Abstract Syntax Tree node. All syntax
    tree nodes represent either a message pass or a constant expression.
    """
    pass


class MsgAstNode(AstNode):
    def __init__(self, target, name, args=None):
        super(MsgAstNode, self).__init__()
        self.target = target
        self.name = name
        self.args = args or []

    def __repr__(self):
        return '<AstNode {target} {name} ({args})>'.format(
            target=self.target,
            name=self.name,
            args=len(self.args),
        )


class ConstAstNode(AstNode):
    def __init__(self, const_value):
        super(ConstAstNode, self).__init__()
        self.const_value = const_value

    def __repr__(self):
        return '<ConstAstNode {}>'.format(self.const_value)
