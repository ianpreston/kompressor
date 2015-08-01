from kompressor.io import IoState, IoMessage
from kompressor.ast import Interpreter
from kompressor.lexer import Lexer
from kompressor.parser import Parser
import kompressor.builtins


def main():
    i = Interpreter()

    # Install builtins
    IoState.root.set_slot('setSlot', kompressor.builtins.SetSlot())
    IoState.root.set_slot('clone', kompressor.builtins.Clone())

    # Bootstrap the global scope
    lobby = IoState.root.clone()
    lobby.set_slot('Object', IoState.root)
    lobby.set_slot('Lobby', lobby)
    IoState.push_frame(IoMessage(lobby, lobby, None))

    # Create the string type
    io_string = IoState.root.clone()
    io_string.set_slot('println', kompressor.builtins.Println())
    lobby.set_slot('String', io_string)

    while True:
        source_line = input('>>>')
        tokens = Lexer(source_line).iter_match_tokens()
        ast_root = Parser(list(tokens)).program()

        i.evaluate_ast_node(ast_root)


if __name__ == '__main__':
    main()
