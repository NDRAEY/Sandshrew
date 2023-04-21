import lexparse
from pprint import pprint
from interp import Interpreter

from ch_modules import print as PrintModule
from ch_modules import trigonometry as TrigModule

def make_ast(code):
    lexer = lexparse.lex(module=lexparse)
    lexer.filename = "<stdio>"
    parser = lexparse.yacc(debug=True, module=lexparse)

    return parser.parse(code)

if __name__=="__main__":
    code = '''
    a(x) = 3x
    
    print(a(2))
    '''

    tot = make_ast(code)

    pprint(tot)

    interp = Interpreter(code)

    interp.add_module(PrintModule.Module)
    interp.add_module(TrigModule.Module)
    
    interp.run(tot)
