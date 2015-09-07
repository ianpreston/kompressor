class SolCode:
    """
    Represents an executable bit of Sol code
    """
    def evaluate(self, state):
        raise NotImplementedError()


class SolCodePass(SolCode):
    """
    Represents a message pass expression
    """
    def __init__(self, target, name, args=None):
        # SolCode object representing how to get the target of this message
        self.target = target

        # Name of the message to be passed to target (str)
        self.name = name

        # List of arguments to this message pass as SolCode instances
        self.args = args or []

    def __repr__(self):
        return '<SolCodePass {self.target}.{self.name}({self.args})>'.format(self=self)


class SolCodeConst(SolCode):
    def __init__(self, const_value):
        self.const_value = const_value

    def __repr__(self):
        return '<SolCodeConst {self.const_value}>'.format(self=self)


class SolCodeBlock(SolCode):
    """
    Represents a block of expressions to execute as a group
    """
    def __init__(self, codes):
        self.codes = codes

    def __repr__(self):
        return '<SolCodeBlock {self.codes}>'.format(self=self)
