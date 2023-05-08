from ply.lex import lex
from ply.yacc import yacc
from errors import LexerError

import math
import sandshrew_ast as AST
from log import Log as log

# TODO: Make deatiled error when lexing and parsing

t_ignore = " \t"
t_PLUS = r"\+"
t_MUL = r"\*"
t_EXPON = r"\^"
t_DIV = r"\/"
t_MINUS = r"\-"
t_ASSIGN = r"\="

t_LESS = r"\<"
t_GREATER = r"\>"

t_PAREN_OPEN  = r"\("
t_PAREN_CLOSE = r"\)"
t_COMMA = r"\,"
t_DOT = r"\."
t_SEMICOLON = r"\;"
t_CURLY_OPEN = r"\{"
t_CURLY_CLOSE = r"\}"
t_ANGLE_OPEN = r"\<"
t_ANGLE_CLOSE = r"\>"
t_QUOTE = "'"
t_ARROW_RIGHT = "->"
t_OR = "\|"
t_FACTOR = "!"

reserved = (
    "LIM", "TRUE", "FALSE", "RETURN"
)

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t

t_STRING = r'"[^"\\]*(?:\\.[^"\\]*)*"'

tokens = ["STRING",
          "INTEGER",
          "PLUS", "MINUS", "MUL", "DIV",
          "ASSIGN",
          "GREATER", "LESS",
          "DOT", "COMMA", "NEWLINE", "SEMICOLON",
          "PAREN_OPEN", "PAREN_CLOSE",
          "ANGLE_OPEN", "ANGLE_CLOSE", "ID",
          "CURLY_OPEN", "CURLY_CLOSE",
          "QUOTE", "ARROW_RIGHT", "FACTOR",
          "EXPON", "OR"
          ] + list(reserved)

on_error = lambda: exit(1)

def t_INTEGER(token):
    r"(0x[\dA-Fa-f]+|0o[0-7]+|0b[10]+|\d+)"
    return token

def t_NEWLINE(token):
    r'\n'
    token.lexer.lineno += 1
    return token

def t_comment_multi(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_comment(t):
    r'\/\/\/?.*'

def t_error(t):
    le = LexerError(t.lexer)
    le.error(t.lexer.filename, f"Неизвестный символ {t.value[0]!r}", t)

    on_error()

# Parser ================================================================

def eval_partial(a, op, b):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "/":
        return a / b
    elif op == "*":
        return a * b
    elif op == "^":
        return a ** b

precedence = (
    ('left', 'GREATER', 'LESS'),
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'MUL'),
    ('left', 'DIV'),
    ('left', 'EXPON'),
    ('left', 'FACTOR'),
    ('left', 'ID'),
    ('right', 'UMINUS'),
)

def p_error(p):
    errtoken = "`"+str(p.value)+"`" if p else "`--неизвестно--`"
    tokentype = p.type if p else "`--неизвестно--`"
    ln = p.lineno if p else 0

    log.error('Синтаксическая ошибка!')
    log.hint(f' Токен: {errtoken} | ID токена: {tokentype} | Строка: {ln}')

    if p is None:
        return

    line = p.lexer.code.split("\n")[ln - 1]

    offset = log.codeline(line, ln)

    lens = map(len, p.lexer.code.split("\n")[:ln - 1])
    lens = sum([i + 1 for i in lens])

    offset -= lens

    print(" "*(offset + p.lexpos), "^", sep='')

    on_error()

def p_program_first(p):
    'program : operation'
    if p[1] and not ((type(p[1]) is AST.Operation) and p[1].op == "\n"):
        p[0] = AST.Program([p[1]])
    else:
        p[0] = AST.Program([])

def p_program(p):
    '''
    program : program operation
    '''
    p[1].ops.append(p[2])
    p[0] = p[1]

def p_operation_end(p):
    """
    operation : operation end
    """
    p[0] = p[1]

def p_operation(p):
              # | fcall
    '''
    operation : expr
              | return
              | assign
              | end
    '''
    p[0] = AST.Operation(p[1], p[1].lineno if hasattr(p[1], 'lineno') else p.lineno(1))

def p_lim_der_fac_expr(p):
    '''
    expr  : limit
          | derivate
          | factorial
          | abs
    '''
    p[0] = p[1]

def p_abs(p):
    '''
    abs : OR expr OR
    '''
    p[0] = AST.Abs(p[2], p[2].lineno)

def p_return(p):
    'return : RETURN expr'
    p[0] = AST.Return(p[2], p.lineno(1))

def p_factorial(p):
    '''
    factorial : expr FACTOR
    '''
    # Optimized variant at parse time
    if type(p[1]) is AST.Integer:
        p[0] = AST.Integer(math.factorial(p[1].value), p[1].lineno, p[1].position)
    else:
        p[0] = AST.Factorial(p[1], p[1].lineno)

def p_deriv(p):
    '''
    derivate : expr QUOTE
    '''
    p[0] = AST.Derivate(p[1], p[1].lineno)

def p_limit(p):
    '''
    limit : LIM ANGLE_OPEN to ANGLE_CLOSE expr
    '''
    p[0] = AST.Limit(p[3], p[5], p.lineno(1))

def p_to(p):
    '''
    to : id ARROW_RIGHT expr
    '''
    p[0] = AST.To(p[1], p[3], p[1].lineno)

def p_fc_expr(p):
    '''
    expr : fcall
    '''
    p[0] = p[1]

def p_function_call(p):
    '''
    fcall : id PAREN_OPEN params PAREN_CLOSE
          | id PAREN_OPEN PAREN_CLOSE
    '''
    if len(p) == 5:
        p[0] = AST.FuncCall(p[1], p[3], p[1].lineno)
    else:
        p[0] = AST.FuncCall(p[1], AST.Params([], p[1].lineno), p[1].lineno)


def p_params(p):
    '''
    params : expr
           | params COMMA expr
    '''
    if len(p) == 2:
        p[0] = AST.Params([p[1]], p[1].lineno)
    else:
        if type(p[1]) is AST.Params:
            p[0] = AST.Params([*p[1].value, p[3]], p[1].lineno)
        else:
            p[0] = AST.Params([p[1], p[3]], p[1].lineno)


def p_hard_func_empty(p):
    'assign : fcall ASSIGN CURLY_OPEN CURLY_CLOSE'
    p[0] = AST.Assign(p[1], AST.Program([]), p[1].lineno)


def p_hard_func(p):
    'assign : fcall ASSIGN CURLY_OPEN program CURLY_CLOSE'
    p[0] = AST.Assign(p[1], p[4], p[1].lineno)


def p_assign(p):
    '''
    assign : id ASSIGN expr
           | fcall ASSIGN expr
    '''
    p[0] = AST.Assign(p[1], p[3], p[1].lineno)


def p_binop(p):
    '''
    expr : expr PLUS expr
         | expr MINUS expr
         | expr MUL expr
         | expr DIV expr
         | expr EXPON expr
    '''
    p[0] = AST.BinOp(p[1], p[2], p[3], p[1].lineno)

    if type(p[1]) == AST.Integer \
       and type(p[3]) == AST.Integer \
       and p[2] != "/":
           p[0] = AST.Integer(
                eval_partial(p[1].value, p[2], p[3].value),
                p[1].lineno,
                p[1].position
            )


def p_expval(p):
    'expr : value'
    p[0] = p[1]


def p_mul_binop(p):
    '''
    expr : number id
    '''
    p[0] = AST.BinOp(p[1], "*", p[2], p.lineno(1))


def p_binop_paren(p):
    '''
    expr : PAREN_OPEN expr PAREN_CLOSE
    '''
    p[0] = p[2]


def p_negative_value(p):
    '''
    expr : MINUS expr %prec UMINUS
    '''
    if isinstance(p[2], AST.Integer):
        p[0] = AST.Integer(-p[2].value, p.lineno(2), p.lexpos(2))
    else:
        # p[0] = AST.Negate(AST.Name(p[2].value, p.lineno(2), p.lexpos(2)), p.lineno(2))
        p[0] = AST.Negate(p[2], p.lineno(2))

def p_value_string(p):
    '''
    value : STRING
    '''
    p[0] = AST.String(p[1][1:-1], p.lineno(1), p.lexpos(1))

def p_value_id(p):
    '''
    value : id
    '''
    p[0] = p[1]

def p_value_bool(p):
    '''
    value : bool
    '''
    p[0] = p[1]

def p_id(p):
    '''
    id : ID
    '''
    p[0] = AST.Name(p[1], p.lineno(1), p.lexpos(1))

def p_bool(p):
    '''
    bool : TRUE
         | FALSE
    '''
    if p[1] == "true":
        p[0] = AST.Bool(True, p.lineno(1), p.lexpos(1))
    else:
        p[0] = AST.Bool(False, p.lineno(1), p.lexpos(1))

def p_value_number(p):
    '''
    value : number
          | float
    '''
    p[0] = p[1]

def p_number(p):
    '''
    number : INTEGER
    '''
    p[0] = AST.Integer(eval(p[1]), p.lineno(1), p.lexpos(1))

def p_float(p):
    '''
    float : INTEGER DOT INTEGER
    '''
    p[0] = AST.Float(float(str(p[1])+"."+str(p[3])), p.lineno(1), p.lexpos(1))

def p_end(p):
    '''
    end : SEMICOLON
        | NEWLINE
    '''
    p[0] = AST.End(p[1], p.lineno(1))

