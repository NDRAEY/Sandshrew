import sys

sys.path.insert(0, "..")

from interp import Interpreter

class Module:
    def __init__(self, ctx):
        self.ctx = ctx
        
        ctx.functions['mul'] = self

    def __call__(self, *args, **kwargs):
        interp = Interpreter(self.ctx.code)
        interp.context = self.ctx

        start, stop, fn = args
        result = 1

        for i in range(start, stop + 1):
            result *= interp.call_func(fn, [i])
        
        return result
