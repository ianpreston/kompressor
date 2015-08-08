import enum
from kompressor.io import IoMessage


class Interpreter:
    def __init__(self, state):
        self.state = state

    def evaluate_const_ast_node(self, node):
        """
        Resolve constant expressions by cloning one of the built-in
        types, such as `String` or `Int`.
        """
        if node.const_type == ConstType.STRING:
            string_clone = self.state.resolve_name('String').clone()
            string_clone.value = node.const_value
            return string_clone

        elif node.const_type == ConstType.INT:
            int_clone = self.state.resolve_name('Int').clone()
            int_clone.value = node.const_value
            return int_clone

    def evaluate_assign_ast_node(self, node):
        """
        Compile assignments into `setSlot` messages
        """
        msg_node = MsgAstNode(
            target='self',
            name='setSlot',
            args=[
                node.ident,
                node.value,
            ]
        )
        return self.evaluate_msg_ast_node(msg_node)

    def evaluate_msg_ast_node(self, node):
        """
        Evaluate message pass expressions with IoState.evaluate()
        """
        sender = self.state.current_context()
        target = self.evaluate_ast_node(node.target)

        # Recursively evaluate this node's arguments, which are themselves
        # message pass expressions
        resolved_args = [self.evaluate_ast_node(arg) for arg in node.args]

        message = IoMessage(sender, target, node.name, resolved_args)
        return self.state.evaluate(message)

    def evaluate_ast_node(self, node):
        if isinstance(node, str):
            return self.state.resolve_name(node)

        elif isinstance(node, ConstAstNode):
            return self.evaluate_const_ast_node(node)

        elif isinstance(node, AssignAstNode):
            return self.evaluate_assign_ast_node(node)

        else:
            return self.evaluate_msg_ast_node(node)


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


class AssignAstNode(AstNode):
    def __init__(self, ident, value):
        super(AssignAstNode, self).__init__()
        self.ident = ident
        self.value = value


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
