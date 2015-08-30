from sol.io import IoMessage
from sol.ast import (
    IdentAstNode,
    MsgAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)


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

    def evaluate_ident_ast_node(self, node):
        return node.ident

    def evaluate_assign_ast_node(self, node):
        """
        Compile assignments into `setSlot` messages
        """
        msg_node = MsgAstNode(
            target=IdentAstNode('self'),
            name=IdentAstNode('setSlot'),
            args=[
                ConstAstNode(
                    ConstType.STRING,
                    self.evaluate_ident_ast_node(node.left)
                ),
                node.right,
            ]
        )
        return self.evaluate_msg_ast_node(msg_node)

    def evaluate_msg_ast_node(self, node):
        """
        Evaluate message pass expressions with IoState.evaluate()
        """
        sender = self.state.current_context()
        target = self.evaluate_ast_node(node.target)
        name = self.evaluate_ident_ast_node(node.name)

        # Recursively evaluate this node's arguments, which are themselves
        # message pass expressions
        resolved_args = [self.evaluate_ast_node(arg) for arg in node.args]

        message = IoMessage(sender, target, name, resolved_args)
        return self.state.evaluate(message)

    def evaluate_ast_node(self, node):
        if isinstance(node, IdentAstNode):
            return self.state.resolve_name(
                self.evaluate_ident_ast_node(node)
            )

        elif isinstance(node, ConstAstNode):
            return self.evaluate_const_ast_node(node)

        elif isinstance(node, AssignAstNode):
            return self.evaluate_assign_ast_node(node)

        else:
            return self.evaluate_msg_ast_node(node)
