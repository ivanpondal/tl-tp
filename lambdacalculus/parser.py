#! coding: utf-8
"""Parser LR(1) de cálculo lambda."""
import ply.yacc as yacc
from .lexer import tokens
from expression import *

def p_expression_succ(p):
    'expression : SUCC_OPEN expression PAR_CLOSE'
    p[0] = p[2].succ()

def p_expression_pred(p):
    'expression : PRED_OPEN expression PAR_CLOSE'
    p[0] = p[2].pred()

def p_expression_iszero(p):
    'expression : ISZERO_OPEN expression PAR_CLOSE'
    p[0] = p[2].is_zero()

def p_expression_ifthenelse(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = p[2].if_else(p[4], p[6])

#def p_expression_lambda(p):
#    'expression : LAMBDA VAR COLON type DOT expression'
#    p[0] = Abstraction(p[2],p[4],p[6])

def p_expression_zero(p):
    'expression : ZERO'
    p[0] = p[1]

def p_expression_bool(p):
    'expression : BOOL'
    p[0] = p[1]

def p_expression_var(p):
    'expression : VAR'
    p[0] = p[1]

def p_error(p):
    print("================\nHubo un error en el parseo:\n" + str(p) + "\n================\n")

    parser.restart()

# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)
