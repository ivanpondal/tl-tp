#! coding: utf-8
"""Parser LR(1) de cálculo lambda."""
import ply.yacc as yacc
from .lexer import tokens
from expression import *

def p_expression_expression_prime(p):
    'expression : expression_prime'
    p[0] = p[1]

def p_expression_application(p):
    'expression : expression expression_prime'
    print p[1]
    p[0] = p[1].apply(p[2])

def p_expression_prime_succ(p):
    'expression_prime : SUCC_OPEN expression PAR_CLOSE'
    p[0] = p[2].succ()

def p_expression_prime_pred(p):
    'expression_prime : PRED_OPEN expression PAR_CLOSE'
    p[0] = p[2].pred()

def p_expression_prime_iszero(p):
    'expression_prime : ISZERO_OPEN expression PAR_CLOSE'
    p[0] = p[2].is_zero()

def p_expression_prime_ifthenelse(p):
    'expression_prime : IF expression THEN expression ELSE expression'
    p[0] = p[2].if_else(p[4], p[6])

def p_expression_prime_abstraction(p):
    'expression_prime : LAMBDA VAR COLON type DOT expression'
    p[0] = Abstraction(p[2], p[4], p[6])

def p_expression_prime_zero(p):
    'expression_prime : ZERO'
    p[0] = p[1]

def p_expression_prime_bool(p):
    'expression_prime : BOOL'
    p[0] = p[1]

def p_expression_prime_var(p):
    'expression_prime : VAR'
    p[0] = p[1]

def p_type(p):
    'type : type_prime'
    p[0] = p[1]

def p_type_prime(p):
    'type_prime : TYPE'
    p[0] = p[1]

def p_error(p):
    print("================\nHubo un error en el parseo:\n" + str(p) + "\n================\n")

    parser.restart()

# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)
