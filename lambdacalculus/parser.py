"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens

#def p_expression_0_abstraction(p):
#    'expression_0 : expression_0 expression_1'

def p_expression_succ(p):
    'expression : SUCC_OPEN expression PAR_CLOSE'
    p[0] = p[2].succ()

def p_expression_nat(p):
    'expression : NAT'
    p[0] = p[1]

def p_expression_bool(p):
    'expression : BOOL'
    p[0] = p[1]

def p_error(p):
    print("Hubo un error en el parseo." + str(p))

    parser.restart()

# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)
