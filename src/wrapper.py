import lexparse
from interp import Interpreter

from ch_modules import print as PrintModule
from ch_modules import trigonometry as TrigModule
from ch_modules import sum as SumModule

def make_ast(code, filename="<stdio>", quiet=False):
    lexer = lexparse.lex(module=lexparse)
    lexer.filename = "<stdio>"
    lexer.code = code
    
    parser = lexparse.yacc(debug=True, module=lexparse, quiet=quiet)

    return parser.parse(code)


def build_interpreter(code, variables={}, functions={}):
    interp = Interpreter(code)

    interp.add_module(PrintModule.Module)
    interp.add_module(TrigModule.Module)
    interp.add_module(SumModule.Module)

    interp.context.variables |= variables
    interp.context.functions |= functions
    
    return interp


def run_code(code, debug=False, variables={}, functions={}):
    ast = make_ast(code, quiet=not debug)
    interp = build_interpreter(code)

    return interp.run(ast)
