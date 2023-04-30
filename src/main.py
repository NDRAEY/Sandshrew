import wrapper
import shell
import argparse
from pprint import pprint

if __name__=="__main__":
    """
    code = '''
    deg2rad(deg) = deg * pi / 180

    sin_my(deg) = {
        rads = deg2rad(deg)

        sin_tailor(x) = (-1) ^ x * ((rads ^ (2x + 1)) / (2x + 1)!)

        return sum(0, 25, sin_tailor)
    }

    print(sin_my(60))
    '''
    """

    argp = argparse.ArgumentParser(prog="charmander")

    argp.add_argument("--debug", "-D", action="store_true", help="Включает вывод отладочной информации")
    argp.add_argument("--show-ast", "-S", action="store_true", help="Показать абстрактное синтаксическое дерево и выйти.")
    argp.add_argument("FILE", nargs='?', help="Файл для исполнения")

    args = argp.parse_args()

    if args.FILE:
       with open(args.FILE, "r") as f:
            code = f.read()
    else:
        if args.show_ast:
            print("Параметр `show_ast` не работает в интерактивной оболочке")

        ishell = shell.Shell()
        ishell.run()

    if args.show_ast:
        pprint(wrapper.make_ast(code))

        exit(0)

    tot = wrapper.run_code(code, debug=args.debug)

    if tot is not None:
        print(tot)
