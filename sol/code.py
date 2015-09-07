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


class SolCodeIdent(SolCode):
    """
    Represents an identifier
    """
    def __init__(self, ident):
        self.ident = ident

    def __repr__(self):
        return '<SolCodeIdent {self.ident}>'.format(self=self)


class SolCodeString(SolCode):
    def __init__(self, const_value):
        self.const_value = const_value

    def __repr__(self):
        return 's"{self.const_value}"'.format(self=self)


class SolCodeInt(SolCode):
    def __init__(self, const_value):
        self.const_value = const_value

    def __repr__(self):
        return 'i"{self.const_value}"'.format(self=self)


class SolCodeBlock(SolCode):
    """
    Represents a block of expressions to execute as a group
    """
    def __init__(self, codes):
        self.codes = codes

    def __repr__(self):
        return '<SolCodeBlock {self.codes}>'.format(self=self)
