from sol.ast import (
    IdentAstNode,
    MsgAstNode,
    AssignAstNode,
    ConstAstNode,
    ConstType,
)
from sol.code import (
    SolCodePass,
    SolCodeConst,
)


class Codegen:
    def __init__(self):
        pass

    def evaluate_const_ast_node(self, node):
        """
        Resolve constant expressions into String.new or Int.new calls
        """
        if node.const_type == ConstType.STRING:
            return SolCodePass(SolCodeConst('String'), 'new', [SolCodeConst(node.const_value)])

        elif node.const_type == ConstType.INT:
            return SolCodePass(SolCodeConst('Int'), 'new', [SolCodeConst(node.const_value)])

    def evaluate_ident_ast_node(self, node):
        return SolCodeConst(node.ident)

    def evaluate_assign_ast_node(self, node):
        # Compile assignments into `setSlot` messages
        return SolCodePass(
            target=SolCodeConst('self'),
            name='setSlot',
            args=[
                SolCodePass(SolCodeConst('String'), 'new', [SolCodeConst(node.left.ident)]),
                self.evaluate_ast_node(node.right),
            ],
        )

    def evaluate_msg_ast_node(self, node):
        return SolCodePass(
            target=self.evaluate_ast_node(node.target),
            name=node.name.ident,
            args=[self.evaluate_ast_node(arg) for arg in node.args],
        )

    def evaluate_ast_node(self, node):
        if isinstance(node, IdentAstNode):
            return self.evaluate_ident_ast_node(node)

        elif isinstance(node, ConstAstNode):
            return self.evaluate_const_ast_node(node)

        elif isinstance(node, AssignAstNode):
            return self.evaluate_assign_ast_node(node)

        else:
            return self.evaluate_msg_ast_node(node)
