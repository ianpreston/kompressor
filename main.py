from kompressor.io import IoState, IoMessage
from kompressor.ast import Interpreter, MsgAstNode, ConstAstNode
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

    i.evaluate_ast_node(
        MsgAstNode('self', 'setSlot', [ConstAstNode('x'), MsgAstNode('String', 'clone')])
    )
    i.evaluate_ast_node(
        MsgAstNode('x', 'setSlot', [ConstAstNode('value'), ConstAstNode('Hello, world!')])
    )
    i.evaluate_ast_node(MsgAstNode(MsgAstNode('Lobby', 'x'), 'println'))


if __name__ == '__main__':
    main()
