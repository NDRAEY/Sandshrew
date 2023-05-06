import lexparse
from interp import Interpreter

from sw_modules import print as PrintModule
from sw_modules import trigonometry as TrigModule
from sw_modules import sum as SumModule
from sw_modules import deriv as DerivModule
from sw_modules import log as LogModule
from sw_modules import round as RoundModule

def make_ast(code, filename="<stdio>", debug=False):
    lexer = lexparse.lex(module=lexparse)
    lexer.filename = "<stdio>"
    lexer.code = code
    
    parser = lexparse.yacc(debug=debug, module=lexparse, quiet=not debug)

    return parser.parse(code)


def build_interpreter(code, variables={}, functions={}, on_error = lambda: exit(1)):
    interp = Interpreter(code, on_error=on_error)

    interp.add_module(PrintModule.Module)
    interp.add_module(TrigModule.Module)
    interp.add_module(SumModule.Module)
    interp.add_module(DerivModule.Module)
    interp.add_module(LogModule.Module)
    interp.add_module(RoundModule.Module)

    interp.context.variables |= variables
    interp.context.functions |= functions
    
    return interp


def run_code(code, debug=False, variables={}, functions={}, filename="<stdio>", on_error = lambda: exit(1)):
    ast = make_ast(code, debug=debug, filename=filename)
    interp = build_interpreter(code, variables=variables, functions=functions, on_error=on_error)

    return interp.run(ast)
