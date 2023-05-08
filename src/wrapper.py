import lexparse
from interp import Interpreter

from sw_modules import print as PrintModule
from sw_modules import trigonometry as TrigModule
from sw_modules import sum as SumModule
from sw_modules import deriv as DerivModule
from sw_modules import log as LogModule
from sw_modules import round as RoundModule
from sw_modules import arcs as ArcsModule
from sw_modules import mul as MulModule
from sw_modules import integral as IntegralModule

def make_ast(code, filename="<stdio>", debug=False, on_error=None):
    if on_error:
        lexparse.on_error = on_error

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
    interp.add_module(ArcsModule.Module)
    interp.add_module(MulModule.Module)
    interp.add_module(IntegralModule.Module)

    interp.context.variables |= variables
    interp.context.functions |= functions
    
    return interp


def run_code(code, debug=False, variables={}, functions={}, filename="<stdio>", on_error = lambda: exit(1)):
    ast = make_ast(code, debug=debug, filename=filename, on_error=on_error)
    interp = build_interpreter(code, variables=variables, functions=functions, on_error=on_error)

    return interp.run(ast)
