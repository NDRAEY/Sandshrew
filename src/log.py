import colorama
from colorama import Fore, Style

colorama.init()

class Log:
    @staticmethod
    def error(message):
        print(Fore.LIGHTRED_EX + "error:" + Style.RESET_ALL, message)

    @staticmethod
    def hint(message):
        print(Fore.MAGENTA + "hint:" + Style.RESET_ALL, message)

    @staticmethod
    def warning(message):
        print(Fore.LIGHTYELLOW_EX + "warning:" + Style.RESET_ALL, message)

    @staticmethod
    def codeline(line: str, lineno: int, offset=8):
        print(" "*offset,
              Fore.MAGENTA + str(lineno) + Style.RESET_ALL,
              "|", line)
        return len(" "*offset) + 1 + len(str(lineno)) + 3
