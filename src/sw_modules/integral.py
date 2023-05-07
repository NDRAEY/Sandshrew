import sys

sys.path.insert(0, "..")
import additional_math.integral as integral
from interp import Interpreter

class Module:
    def __init__(self, ctx):
        self.ctx = ctx
        
        ctx.functions['integral'] = self._integral

    def _integral(self, start, end, fn):
        interp = Interpreter(self.ctx.code)
        interp.context = self.ctx

        # print(start, end, fn)

        result = lambda x: interp.call_func(
            fn,
            [x]
        )

        return integral.trapezoidal_rule(
            result,
            start,
            end
        )
