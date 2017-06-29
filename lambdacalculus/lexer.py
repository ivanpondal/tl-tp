#! coding: utf-8
import ply.lex as lex
from expression import *

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
    'VAR',
    'TYPE',
    'SUCC_OPEN',
    'PRED_OPEN',
    'ISZERO_OPEN',
    'PAR_OPEN',
    'PAR_CLOSE',
    'IF',
    'THEN',
    'ELSE'
)

t_PAR_OPEN = r'\('
t_PAR_CLOSE = r'\)'
t_ignore = ' \t'

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
    t.value = Bool(True if t.value == 'true' else False)
    return t

def t_ZERO(t):
    r'0'
    t.value = Zero()
    return t

def t_TYPE(t):
    r'Bool|Nat'
    return t

def t_VAR(t):
    r'[a-z]\w*'
    t.value = Variable(t.value)
    return t

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
