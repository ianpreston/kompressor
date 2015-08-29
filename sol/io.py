class IoRuntimeError(Exception):
    pass


class IoMessage:
    """
    IoMessage represents an in-progress (or past) message pass action
    """
    def __init__(self, sender, target, name, args=None):
        self.sender = sender
        self.target = target
        self.name = name
        self.args = args or []


class IoState:
    def __init__(self, root_object):
        # The `root` is the IoObject of which all other objects
        # will be clones
        self.root = root_object

        # Initialize the call stack, i.e. the stack of message passes
        self.stack = []
        self.push_frame(IoMessage(self.root, self.root, None))

    def push_frame(self, message):
        self.stack.append(message)

    def pop_frame(self):
        self.stack.pop()

    def current_frame(self):
        return self.stack[-1]

    def current_context(self):
        return self.current_frame().sender

    def resolve_name(self, object_name):
        if object_name == 'self':
            return self.current_context()

        resolved = self.current_context().get_slot(object_name)
        if resolved is None:
            raise IoRuntimeError('Could not resolve name', object_name)

        return resolved

    def evaluate(self, message):
        self.push_frame(message)

        slot_value = message.target.get_slot(message.name)
        if not slot_value:
            raise IoRuntimeError('Slot does not exist on target', message.name, message.target)

        if hasattr(slot_value, 'activate'):
            slot_value = slot_value.activate()
        if hasattr(slot_value, '__call__'):
            slot_value = slot_value()

        self.pop_frame()
        return slot_value
