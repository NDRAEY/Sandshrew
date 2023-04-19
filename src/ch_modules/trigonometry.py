import math

class Module:
    def __init__(self, ctx):
        ctx.functions['sin'] = math.sin
        ctx.functions['cos'] = math.cos
        ctx.functions['tan'] = math.tan
        ctx.variables['pi']  = math.pi

        self.arg_count = 1
