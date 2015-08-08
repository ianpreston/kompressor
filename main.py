from kompressor.io import IoState, IoMessage
from kompressor.object import IoObject
from kompressor.ast import Interpreter
from kompressor.lexer import Lexer
from kompressor.parser import Parser


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


def main():
    root = IoObject()
    state = IoState(root)
    i = Interpreter(state)

    # Bootstrap the object system
    io_string = root.clone()
    io_int = root.clone()
    root.set_slot('Object', root)
    root.set_slot('String', io_string)
    root.set_slot('Int', io_int)

    # Initialize builtin slots
    patch_object(root, state)
    patch_string(io_string, state)

    # Bootstrap the global scope
    lobby = root.clone()
    root.set_slot('Lobby', lobby)
    lobby.set_slot('Lobby', lobby)
    state.push_frame(IoMessage(lobby, lobby, None))

    while True:
        source_line = input('>>>')
        tokens = Lexer(source_line).iter_match_tokens()
        ast_root = Parser(list(tokens)).program()

        i.evaluate_ast_node(ast_root)


if __name__ == '__main__':
    main()
