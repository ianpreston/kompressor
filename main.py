from kompressor.io import IoState, IoMessage
from kompressor.object import IoObject
from kompressor.ast import Interpreter
from kompressor.lexer import Lexer
from kompressor.parser import Parser
from kompressor.builtin import apply_builtins


def main():
    root = IoObject()
    state = IoState(root)
    i = Interpreter(state)

    # Bootstrap builtin objects and slots
    apply_builtins(state)

    # Bootstrap the global scope
    lobby = root.clone()
    root.set_slot('Object', root)
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
