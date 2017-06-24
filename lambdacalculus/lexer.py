#! coding: utf-8
import ply.lex as lex

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
    'NAT',
    'VAR',
    'TYPE'
)

t_ignore = ' \t'

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_NAT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TYPE(t):
    r'Bool|Nat'
    return t

def t_VAR(t):
    r'[a-z]\w*'
    return t

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
