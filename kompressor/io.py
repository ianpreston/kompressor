class IoRuntimeError(Exception):
    pass


class IoObject:
    """
    IoObject represents any Object in the runtime
    """
    def __init__(self):
        self.ident = id(self)
        self.slots = {
            'clone': IoObject.builtin_clone,
            'setSlot': IoObject.builtin_set_slot,
        }
        self.proto = None

    def get_slot(self, name):
        return self.slots.get(name)

    def set_slot(self, name, value):
        self.slots[name] = value

    def clone(self):
        clone = IoObject()
        clone.proto = self
        clone.slots = dict(self.slots)
        return clone

    @classmethod
    def builtin_clone(self):
        return self.clone()

    @classmethod
    def builtin_set_slot(self):
        message = IoState.current_frame()
        slot_name = message.args[0]
        slot_value = message.args[1]

        # Grab the Python basestring value from the IoString `slot_name`
        slot_name = slot_name.value

        message.target.set_slot(slot_name, slot_value)
        return slot_value

    def __repr__(self):
        return '<IoObject {}>'.format(self.ident)


class IoString(IoObject):
    """
    Builtin Object type: IoString is a primitive Object type representing
    a Unicode string
    """
    def __init__(self, default=None):
        super(IoString, self).__init__()
        self.value = default or u''
        self.slots.update({
            'println': IoString.builtin_println,
        })

    @classmethod
    def builtin_println(self):
        message = IoState.current_frame()
        value = message.target.value
        print(value)
        return value

    def __repr__(self):
        return u'<IoString {}>'.format(self.value)


class IoInt(IoObject):
    """
    Builtin Object type: IoObject wrapper for an integer
    """
    def __init__(self, default=None):
        super(IoInt, self).__init__()
        self.value = default or 0

    def __repr__(self):
        return u'<IoInt {}>'.format(self.value)


class IoMessage:
    """
    IoMessage represents an in-progress (or past) message pass action
    """
    def __init__(self, sender, target, name, args=None):
        self.sender = sender
        self.target = target
        self.name = name
        self.args = args or []


class _IoState:
    def __init__(self):
        # The `root` is the IoObject of which all other objects
        # will be clones
        self.root = IoObject()

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


IoState = _IoState()
