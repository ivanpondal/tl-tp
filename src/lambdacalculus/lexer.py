#! coding: utf-8
import ply.lex as lex
from expression import *
from exp_type import *
from . import LambdaError

"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

Sí, es súper nigromántico pero es lo que hay.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como se
muestra aquí abajo.

"""

tokens = (
    'BOOL',
    'ZERO',
    'NAT',
    'VAR',
    'TYPE',
    'SUCC_OPEN',
    'PRED_OPEN',
    'ISZERO_OPEN',
    'PAR_CLOSE',
    'IF',
    'THEN',
    'ELSE',
    'LAMBDA',
    'COLON',
    'DOT',
    'PAR_OPEN',
    'ARROW'
)

t_PAR_CLOSE = r'\)'
t_PAR_OPEN = r'\('
t_ignore = ' \t'
t_ARROW = '->'

def t_SUCC_OPEN(t):
    r'succ\('
    return t

def t_PRED_OPEN(t):
    r'pred\('
    return t

def t_ISZERO_OPEN(t):
    r'iszero\('
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_BOOL(t):
    r'true|false'
    t.value = BoolValue(True if t.value == 'true' else False)
    return t

def t_ZERO(t):
    r'0'
    t.value = Zero()
    return t

def t_TYPE(t):
    r'Bool|Nat'
    t.value = BoolType() if t.value == 'Bool' else NatType()
    return t

def t_LAMBDA(t):
    r'\\'
    return t

def t_COLON(t):
    r':'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_VAR(t):
    r'[a-z]\w*'
    t.value = Variable(t.value)
    return t

def t_NAT(t):
    r'\d+'
    number = int(t.value)
    t.value = Zero()
    for i in range(number):
        t.value = Succ(t.value)
    return t

def t_error(t):
    spaces = ' ' * (t.lexpos + 3) # 3 is the prompt length
    raise LambdaLexError("{0}^\n{0}|\n{0}|\nERROR: Illegal character '{1}' at position {2}".\
        format(spaces,t.value[0],t.lexpos))

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)

class LambdaLexError(LambdaError):
    pass