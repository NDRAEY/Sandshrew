class Context:
    def __init__(self, funcs={}, variables={}):
        self.functions = funcs
        self.variables = variables

    def clear(self):
        self.functions = {}
        self.variables = {}
