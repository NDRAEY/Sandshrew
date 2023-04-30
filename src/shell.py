import wrapper
from context import Context

class Shell:
    def __init__(self):
        self.context = Context("")
        self.interp = wrapper.build_interpreter(self.context.code)
        self.interp.context = self.context
        self.linenum = 1

    def run(self):
        while True:
            self.context.code = input(f"{self.linenum}: > ")

            if self.context.code.strip() == "exit":
                exit(0)
            
            self.interp.codelines = self.interp.gencodelines()
            self.linenum += 1

            result = self.interp.run(
                wrapper.make_ast(self.context.code, quiet=True)
            )

            if result is not None:
                print(result)
