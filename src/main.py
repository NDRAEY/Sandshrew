import lexparse
from pprint import pprint
from interp import Interpreter

from ch_modules import print as PrintModule
from ch_modules import trigonometry as TrigModule

if __name__=="__main__":
    code = '''
    a(x) = -x + 1
    
    print(a(2))
    '''

    lexer = lexparse.lex(module=lexparse)
    lexer.filename = "<stdio>"
    parser = lexparse.yacc(debug=True, module=lexparse)

    """
    lexer.input(code)
    while True:
        t = lexer.token()
        if not t: break
        print(t)
    exit(1)
    """

    tot = parser.parse(code)

    pprint(tot)

    interp = Interpreter(code)

    interp.add_module(PrintModule.Module)
    interp.add_module(TrigModule.Module)
    
    interp.run(tot)
