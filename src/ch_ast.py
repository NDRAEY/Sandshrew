from dataclasses import dataclass
from typing import Any

@dataclass
class Program:
    ops: list

@dataclass
class Integer:
    value: int
    lineno: int
    position: int

    def __add__(a, b):
        return Integer(a.value + b.value, a.lineno, a.position)

@dataclass
class Abs:
    value: Any
    lineno: int

@dataclass
class BinOp:
    left: Any
    op: str
    right: Any
    lineno: int

@dataclass
class Operation:
    op: Any
    lineno: int

@dataclass
class Assign:
    name: str
    value: Any
    lineno: int

@dataclass
class Name:
    value: str
    lineno: int
    position: int

@dataclass
class Params:
    value: list
    lineno: int

@dataclass
class FuncCall:
    name: Name
    arguments: Params
    lineno: int

@dataclass
class To:
    name: Name
    value: Any
    lineno: int

@dataclass
class Limit:
    to: To
    equation: Any
    lineno: int

@dataclass
class Derivate:
    value: Any
    lineno: int

@dataclass
class Factorial:
    value: Any
    lineno: int

@dataclass
class Float:
    value: float
    lineno: int
    position: int

@dataclass
class Func:
    name: Name
    args: Params
    code: BinOp
    lineno: int

@dataclass
class String:
    string: str
    lineno: int
    position: int

@dataclass
class Negate:
    value: Any
    lineno: int

@dataclass
class Return:
    value: Any
    lineno: int

@dataclass
class End:
    value: str
    lineno: int
