import enum
from kompressor.io import IoMessage


class Interpreter:
    def __init__(self, state):
        self.state = state

    def evaluate_ast_node(self, node):
        if isinstance(node, str):
            return self.state.resolve_name(node)

        if isinstance(node, ConstAstNode):
            if node.const_type == ConstType.STRING:
                string_clone = self.state.root.get_slot('String').clone()
                string_clone.value = node.const_value
                return string_clone

            elif node.const_type == ConstType.INT:
                string_clone = self.state.root.get_slot('Int').clone()
                string_clone.value = node.const_value
                return string_clone

        sender = self.state.current_context()
        target = self.evaluate_ast_node(node.target)

        # Recursively evaluate this node's arguments, which are themselves
        # message pass expressions
        resolved_args = [self.evaluate_ast_node(arg) for arg in node.args]

        message = IoMessage(sender, target, node.name, resolved_args)
        return self.state.evaluate(message)


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
        return '<MsgAstNode {target} {name} {args}>'.format(
            target=self.target,
            name=self.name,
            args=self.args,
        )


class ConstAstNode(AstNode):
    def __init__(self, const_type, const_value):
        super(ConstAstNode, self).__init__()
        self.const_type = const_type
        self.const_value = const_value

    def __repr__(self):
        return '<ConstAstNode {} {}>'.format(self.const_type, self.const_value)


class ConstType(enum.Enum):
    STRING = 0
    INT = 1
