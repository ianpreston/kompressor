def apply_builtins(state):
    io_string = state.root.clone()
    io_int = state.root.clone()

    patch_object(state.root, state)
    patch_string(io_string, state)
    patch_int(io_int, state)

    state.root.slots.update({
        'String': io_string,
        'Int': io_int,
    })


def patch_object(io_object, state):
    def builtin_set_slot():
        message = state.current_frame()
        slot_name = message.args[0]
        slot_value = message.args[1]

        # Grab the Python basestring value from the IoObject `slot_name`
        slot_name = slot_name.value

        message.target.set_slot(slot_name, slot_value)
        return slot_value

    def builtin_clone():
        target = state.current_frame().target
        clone = target.clone()
        clone.proto = target
        clone.slots = dict(target.slots)
        return clone

    io_object.slots.update({
        'clone': builtin_clone,
        'setSlot': builtin_set_slot,
    })


def patch_string(io_string, state):
    def println():
        value = state.current_frame().target.value
        print(value)
        return value

    io_string.slots.update({
        'println': println,
    })


def patch_int(io_int, state):
    pass
