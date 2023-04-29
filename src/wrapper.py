import lexparse
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


def build_interpreter(code):
    interp = Interpreter(code)

    interp.add_module(PrintModule.Module)
    interp.add_module(TrigModule.Module)
    interp.add_module(SumModule.Module)
    
    return interp

def run_code(code, show_ast=False):
    ast = make_ast(code)
    interp = build_interpreter(code)

    return interp.run(ast)
