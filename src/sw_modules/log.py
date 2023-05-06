import math

class Module:
    def __init__(self, ctx):
        ctx.functions['log'] = self.log
        ctx.functions['lg'] = math.log10
        ctx.functions['ln'] = self.ln

        ctx.variables['e'] = math.e

    def log(self, base, value):
        return math.log(value, base)

    def ln(self, value):
        return math.log(value)
