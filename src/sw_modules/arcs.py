import math
import sys

sys.path.insert(0, "..")
import additional_math.integral as integral

class Module:
    def __init__(self, ctx):
        ctx.functions['arcsin'] = self.arcsin
        ctx.functions['arccos'] = self.arccos
        ctx.functions['arctan'] = self.arctan
        ctx.functions['arctg']  = self.arctan

    def arcsin(self, x):
        "arcsin(x) = integral from 0 to x of (1 - t^2)^(-1/2)dt"
        return integral.trapezoidal_rule(
            lambda t: (1 - t**2)**(-1/2),
            0,
            x
        )

    def arccos(self, x):
        "arccos(x) = pi/2 - arcsin(x)"
        return math.pi / 2 - self.arcsin(x)

    def arctan(self, x):
        "arctan(x) = integral from 0 to x of (1 + t^2)^(-1) dt"
        return integral.trapezoidal_rule(
            lambda t: (1 + t**2) ** (-1),
            0,
            x
        )
