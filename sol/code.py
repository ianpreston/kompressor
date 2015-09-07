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
        # Target of this message. Either a str (identifier) or a
        # SolCode object that should be resolved to get the target.
        self.target = target

        # Name of the message to be passed (str)
        self.name = name

        # List of arguments to this message pass, ([SolCode])
        self.args = args or []

    def __repr__(self):
        return '<SolCodePass {self.target}.{self.name}({self.args})>'.format(self=self)


class SolCodeConst(SolCode):
    def __init__(self, const_value):
        self.const_value = const_value


class SolCodeIdentifier(SolCode):
    def __init__(self, identifier):
        self.identifier = identifier


class SolCodeBlock(SolCode):
    """
    Represents a block of expressions to execute as a group
    """
    def __init__(self, codes):
        self.codes = codes

    def __repr__(self):
        return '<SolCodeBlock {self.codes}>'.format(self=self)
