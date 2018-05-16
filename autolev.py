import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from AutolevLexer import AutolevLexer
from AutolevParser import AutolevParser
from myListener import myListener

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    lexer = AutolevLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = AutolevParser(token_stream)
    tree = parser.prog()

    lisp_tree_str = tree.toStringTree(recog=parser)
    #print(lisp_tree_str)

    listener = myListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    print(listener.getSymbolTable())
