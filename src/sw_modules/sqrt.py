import math

class Module:
    def __init__(self, ctx):
        ctx.functions['sqrt'] = math.sqrt
