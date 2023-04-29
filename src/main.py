import lexparse
from pprint import pprint
from interp import Interpreter

from ch_modules import print as PrintModule
from ch_modules import trigonometry as TrigModule
from ch_modules import sum as SumModule

def make_ast(code):
    lexer = lexparse.lex(module=lexparse)
    lexer.filename = "<stdio>"
    lexer.code = code
    parser = lexparse.yacc(debug=True, module=lexparse)

    return parser.parse(code)

if __name__=="__main__":
    code = '''
    deg2rad(deg) = deg * pi / 180

    sin_my(deg) = {
        rads = deg2rad(deg)

        sin_tailor(x) = (-1) ^ x * ((rads ^ (2x + 1)) / (2x + 1)!)

        return sum(0, 25, sin_tailor)
    }

    print(sin_my(60))
    '''

    tot = make_ast(code)

    pprint(tot)

    interp = Interpreter(code)

    interp.add_module(PrintModule.Module)
    interp.add_module(TrigModule.Module)
    interp.add_module(SumModule.Module)
    
    interp.run(tot)
