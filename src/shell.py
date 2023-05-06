import wrapper
from context import Context

class Shell:
    def __init__(self):
        self.context = Context("")
        self.interp = wrapper.build_interpreter(self.context.code, on_error=self.run)
        self.interp.context = self.context
        self.linenum = 1

    def run(self):
        while True:
            self.interp.context.code = input(f"[{self.linenum}]: > ")
            if self.interp.context.code == "":
                continue

            print("Set", self.interp.context.code)

            if self.interp.context.code.strip() == "exit":
                exit(0)
            
            self.interp.codelines = self.interp.gencodelines()
            print("Gen")
            
            self.linenum += 1

            result = self.interp.run(
                wrapper.make_ast(self.interp.context.code, debug=False)
            )

            if result is not None:
                print(result)
