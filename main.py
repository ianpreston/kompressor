from kompressor.io import IoState, IoMessage
from kompressor.ast import Interpreter
from kompressor.lexer import Lexer
from kompressor.parser import Parser


def main():
    i = Interpreter()

    # Bootstrap the global scope
    lobby = IoState.root.clone()
    lobby.set_slot('Object', IoState.root)
    lobby.set_slot('Lobby', lobby)
    IoState.push_frame(IoMessage(lobby, lobby, None))

    while True:
        source_line = input('>>>')
        tokens = Lexer(source_line).iter_match_tokens()
        ast_root = Parser(list(tokens)).program()

        i.evaluate_ast_node(ast_root)


if __name__ == '__main__':
    main()
