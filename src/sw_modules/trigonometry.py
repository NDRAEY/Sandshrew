import math

class Module:
    def __init__(self, ctx):
        ctx.functions['sin'] = math.sin
        ctx.functions['cos'] = math.cos
        ctx.functions['tan'] = math.tan
        ctx.functions['tg'] = math.tan

        ctx.functions['deg2rad'] = lambda x: x * math.pi / 180
        ctx.functions['rad2deg'] = lambda x: x * (180 / math.pi)

        ctx.variables['pi']  = math.pi
