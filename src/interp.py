import math
from context import Context
from log import Log as log
import ch_ast as AST
from pprint import pprint
from copy import deepcopy
from typing import Any

from derivate import derivate
from limits import limit

class Interpreter:
    def __init__(self, code: str,
                       context: Context = Context()):

        self.context = context
        self.codelines = code.split('\n')

    def __getcodeline(self, ln: int) -> str:
        return self.codelines[ln - 1] if ln > 0 and ln - 1 < len(self.codelines) else "*неверный номер строки*"

    def __error(self, op, msg: str) -> None:
        log.error(msg)
        print("-" * 5, ": ", f"На строке {op.lineno}", sep='')
        log.codeline(self.__getcodeline(op.lineno), op.lineno, 5)
        exit(1)

    def __binop_eval(self, binop) -> Any:
        if type(binop) is AST.Integer or type(binop) is AST.Float:
            return binop.value
        elif type(binop) is AST.String:
            return binop.string
        elif type(binop) is AST.Factorial:
            return math.factorial(self.__binop_eval(binop.value))
        elif type(binop) is AST.Name:
            value = self.__get_variable_value(binop, binop.value)
            
            return self.__particular_eval(value)
        elif type(binop) is AST.FuncCall:
            return self.__start_func_call(binop.name, binop.arguments)
        elif type(binop) is AST.Negate:
            return -self.__binop_eval(binop.value)
        elif type(binop) is AST.Abs:
            result = abs(self.__binop_eval(binop.value))
            
            if not (type(result) is int):
                self.__error(binop, f"Попытка округления неподдерживаемого типа. ({type(result).__name__})")

            return result
        elif type(binop) is AST.Derivate:
            self.__error(binop, "Невозможно использовать производную рядом с выражением.")
        elif type(binop) is AST.Limit:
            partial_fun = lambda x: self.__particular_eval(self.__func_call_by_function(
                AST.Func(
                    AST.Name("_", -1, -1),
                    AST.Params([AST.Name('x', -1, -1)], -1),
                    binop.equation,
                    -1
                ),
                [AST.Integer(x, -1, -1)],
                binop.equation
            ))

            return limit(partial_fun, binop.to.value.value)

        op = binop.op
        left = binop.left
        right = binop.right

        eleft = self.__binop_eval(left)
        eright = self.__binop_eval(right)

        tle = type(eleft).__name__
        tre = type(eright).__name__

        n1 = tle in ("int", "float")
        n2 = tre in ("int", "float")

        if tle != tre and (not n1) and (not n2):
            self.__error(left, f"Несовместимые типы для операции `{op}`: {tle} и {tre}")
         
        if op == "+":
            return eleft + eright
        elif op == "-":
            return eleft - eright
        elif op == "*":
            return eleft * eright
        elif op == "^":
            return eleft ** eright
        elif op == "/":
            return eleft / eright

    def __particular_eval(self, elem):
        if (type(elem) is AST.Name) \
           or (type(elem) is AST.Integer) \
           or (type(elem) is AST.Float):
            return elem.value
        elif type(elem) is int \
           or (type(elem) is float) \
           or (type(elem) is str):
            return elem
        elif type(elem) is AST.BinOp:
            return self.__binop_eval(elem)
        elif type(elem) is AST.Abs:
            return abs(self.__binop_eval(elem))
        elif type(elem) is AST.String:
            return elem.string
        elif type(elem) is AST.Derivate:
            return self.func2deriv(elem.value)
        elif type(elem) is AST.Limit:
            return self.__binop_eval(elem)

        else:
            print("WARNING: Unevaluable type:", type(elem))
            return elem

    def __get_variable_value(self, op, name: str):
        if name not in self.context.variables:
            self.__error(op, f"Переменная `{name}` не найдена!!!")

        return self.context.variables[name]

    def __start_func_call(self, name: AST.Name, args: AST.Params):
        realname = name.value
        
        if realname not in self.context.functions:
            self.__error(name, f"Функция `{realname}` не найдена!")

        compiled_args = []

        for i in args.value:
            if type(i) is AST.Name:
                value = self.__get_variable_value(i, i.value)
                value = self.__particular_eval(value)

                compiled_args.append(value)
            elif (type(i) is AST.Integer) \
                 or (type(i) is AST.Float):
                    compiled_args.append(i.value)
            elif type(i) is AST.BinOp:
                compiled_args.append(self.__particular_eval(i))
            elif type(i) is AST.Derivate:
                compiled_args.append(self.__particular_eval(i))
            elif type(i) is AST.Abs:
                compiled_args.append(self.__particular_eval(i))
            elif type(i) is AST.FuncCall:
                compiled_args.append(self.__start_func_call(
                    i.name,
                    i.arguments
                ))
            elif type(i) is AST.String:
                compiled_args.append(i.string)
            else:
                print("Trying to add", type(i), "to args")

        # print("ARGS:", args.value)

        fn = self.context.functions[realname]

        return self.__func_call_by_function(fn, compiled_args, name)
        # pprint(compiled_args)

    def __func_call_by_function(self, fn: AST.Func, args: list, fcall: AST.FuncCall = None):
        if type(fn) is not AST.Func:
            # print("Function", realname, "is built-in")
            return fn(*args)
        else:
            accepts = [self.__particular_eval(i) for i in fn.args.value]

            if len(accepts) != len(args):
                self.__error(fcall, f"Несовпадающее число аргументов (прнимает: {len(accepts)} вместо {len(args)})")

            oldctx = deepcopy(self.context)
            
            # Construct
            for nm, v in zip(accepts, args):
                # print(nm, "=", v)
                self.context.variables[nm] = v

            res = self.run(fn.code)

            # Destruct
            for nm, v in zip(accepts, args):
                if nm in self.context.variables:
                    del self.context.variables[nm]

            self.context = oldctx

            return res

    def add_module(self, module_class):
        module_class(self.context)

    def func2deriv(self, deriv):
        partial_fun = lambda x: self.__func_call_by_function(
            AST.Func(
                AST.Name("_", -1, -1),
                AST.Params([AST.Name('x', -1, -1)], -1),
                deriv,
                -1
            ),
            [AST.Integer(x, -1, -1)],
            deriv
        )

        return derivate(
            partial_fun,
            1
        )

    def run(self, ast):
        if type(ast) is AST.Name:
            return self.__get_variable_value(ast, ast.value)
        elif type(ast) is AST.BinOp:
            return self.__binop_eval(ast)
        elif type(ast) is AST.Integer:
            return ast.value
        elif type(ast) is AST.Factorial:
            return math.factorial(self.__binop_eval(ast.value))
        elif type(ast) is AST.Derivate:
            func = ast.value

            # Create temporal function
            partial_fun = lambda x: self.__func_call_by_function(
                AST.Func(
                    AST.Name("_", -1, -1),
                    AST.Params([AST.Name('x', -1, -1)], -1),
                    func,
                    -1
                ),
                [AST.Integer(x, -1, -1)],
                func
            )

            d = derivate(
                partial_fun,
                1
            )

            return d
        elif type(ast) is AST.FuncCall:
            return self.__start_func_call(ast.name, ast.arguments)
        elif type(ast) is AST.Negate:
            return -self.__binop_eval(ast.value)
        elif type(ast) is not AST.Program:
            self.__error(ast, "Неизвестный тип возврата: "+str(type(ast))+"  "+str(ast))

        ops = ast.ops

        for i in ops:
            op = i.op

            op_type = type(op)

            if op_type is AST.End:
                continue
            elif op_type is AST.Assign:
                name = op.name
                val  = op.value

                if type(name) is AST.Name:
                    tmp = self.__particular_eval(name)
                    self.context.variables[tmp] = self.__particular_eval(val)
                elif type(name) is AST.FuncCall:
                    rname = self.__particular_eval(name.name)
                    args = name.arguments
                    
                    self.context.functions[rname] = AST.Func(
                        name.name,
                        args,
                        val,
                        name.name.lineno
                    )
                else:
                    print("Support in Interpreter::run(): ", type(name))
                    exit(1)
            elif op_type is AST.FuncCall:
                self.__start_func_call(op.name, op.arguments)
            else:
                self.__error(op, f"Неизвестная операция класса: {op_type}")

            # print("=>", op_type)
