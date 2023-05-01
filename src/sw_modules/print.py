class Module:
    def __init__(self, ctx):
        ctx.functions['print'] = self

    def __call__(self, *args, **kwargs):
        print(*args)
