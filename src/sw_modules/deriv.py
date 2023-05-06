import sys

sys.path.insert(0, "..")

import additional_math.derivate as deriv

from interp import Interpreter

class Module:
    def __init__(self, ctx):
        self.ctx = ctx
    
        ctx.functions['deriv'] = self

    def __call__(self, func, x, precision=1e-8):
        interp = Interpreter(self.ctx.code)
        interp.context = self.ctx
        
        return deriv.derivate(
            lambda w: interp.call_func(func, [w]),
            x,
            precision
        )
