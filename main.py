import traceback
from sol.io import IoState, IoMessage
from sol.object import IoObject
from sol.lexer import Lexer
from sol.parser import SolParser
from sol.builtin import apply_builtins
from sol.codegen import Codegen
from sol.runtime import Runtime


def main():
    root = IoObject()
    state = IoState(root)
    codegen = Codegen()
    runtime = Runtime(state)

    # Bootstrap builtin objects and slots
    apply_builtins(state)

    # Bootstrap the global scope
    lobby = root.clone()
    root.set_slot('Object', root)
    root.set_slot('Lobby', lobby)
    lobby.set_slot('Object', root)
    lobby.set_slot('Lobby', lobby)
    state.push_frame(IoMessage(lobby, lobby, None))

    while True:
        source_line = input('>>>')
        try:
            tokens = Lexer(source_line).iter_match_tokens()

            ast_root = SolParser(list(tokens)).program()
            code = codegen.evaluate_ast_node(ast_root)
            runtime.evaluate(code)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    main()
