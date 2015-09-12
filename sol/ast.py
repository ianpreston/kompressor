import enum


class AstNode:
    """
    AstNode represents a parsed Abstract Syntax Tree node. All syntax
    tree nodes represent either a message pass or a constant expression.
    """
    pass


class ProgramAstNode(AstNode):
    def __init__(self, root):
        super(ProgramAstNode, self).__init__()
        self.root = root


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


class IdentAstNode(AstNode):
    def __init__(self, ident):
        super(IdentAstNode, self).__init__()
        self.ident = ident

    def __repr__(self):
        return '<IdentAstNode {ident}>'.format(ident=self.ident)


class AssignAstNode(AstNode):
    def __init__(self, left, right):
        super(AssignAstNode, self).__init__()
        self.left = left
        self.right = right

    def __repr__(self):
        return '<AssignAstNode {left} := {right}>'.format(
            left=self.left,
            right=self.right,
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
