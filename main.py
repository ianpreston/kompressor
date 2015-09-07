import traceback
from sol.state import SolState, SolMessage
from sol.object import SolObject
from sol.lexer import Lexer
from sol.parser import SolParser
from sol.builtin import apply_builtins
from sol.codegen import Codegen
from sol.runtime import Runtime


def main():
    root = SolObject()
    state = SolState(root)
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
    state.push_frame(SolMessage(lobby, lobby, None))

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
