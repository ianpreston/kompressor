from sol.state import SolMessage
from sol.code import (
    SolCodePass,
    SolCodeIdent,
    SolCodeString,
    SolCodeInt,
    SolCodeBlock,
)


class Runtime:
    def __init__(self, state):
        self.state = state

    def evaluate(self, code):
        # TODO - Dat OOP doe
        if isinstance(code, SolCodePass):
            return self.evaluate_pass(code)
        elif isinstance(code, SolCodeIdent):
            return self.evaluate_ident(code)
        elif isinstance(code, SolCodeString) or isinstance(code, SolCodeInt):
            return self.evaluate_const(code)
        elif isinstance(code, SolCodeBlock):
            return self.evaluate_block(code)

        raise Exception('Invalid argument to Runtime.evaluate', code)

    def evaluate_pass(self, code):
        sender = self.state.current_context()
        target = self.evaluate(code.target)
        name = code.name

        resolved_args = [
            self.evaluate(arg)
            for arg in code.args
        ]

        message = SolMessage(sender, target, name, resolved_args)
        return self.state.evaluate(message)

    def evaluate_ident(self, code):
        return self.state.resolve_name(code.ident)

    def evaluate_const(self, code):
        return code.const_value

    def evaluate_block(self, code):
        raise NotImplementedError()
