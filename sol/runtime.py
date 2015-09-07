from sol.object import IoObject
from sol.io import IoMessage
from sol.code import (
    SolCodePass,
    SolCodeConst,
    SolCodeBlock,
)


class Runtime:
    def __init__(self, state):
        self.state = state

    def evaluate(self, code):
        # TODO - Dat OOP doe
        if isinstance(code, SolCodePass):
            return self.evaluate_pass(code)
        elif isinstance(code, SolCodeConst):
            return self.evaluate_const(code)
        elif isinstance(code, SolCodeBlock):
            return self.evaluate_block(code)

        raise Exception('Invalid argument to Runtime.evaluate', code)

    def evaluate_pass(self, code):
        sender = self.state.current_context()
        target = self.resolve_pass_target(code.target)
        name = code.name

        resolved_args = [
            self.evaluate(arg)
            for arg in code.args
        ]

        message = IoMessage(sender, target, name, resolved_args)
        return self.state.evaluate(message)

    def resolve_pass_target(self, target):
        if isinstance(target, str):
            return self.state.resolve_name(target)

        if isinstance(target, IoObject):
            return target

        return self.resolve_pass_target(self.evaluate(target))

    def evaluate_const(self, code):
        return code.const_value

    def evaluate_block(self, code):
        raise NotImplementedError()
