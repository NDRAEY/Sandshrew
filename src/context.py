class Context:
    def __init__(self, code, funcs={}, variables={}):
        self.functions = funcs
        self.variables = variables
        self.code = code

    def clear(self):
        self.functions = {}
        self.variables = {}
