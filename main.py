from lambdacalculus import parser

while True:
    try:
        exp_str = raw_input('labdacalculus> ')
    except EOFError:
        break
    ast = parser.apply_parser(exp_str)
    print(str(ast.reduce()) + " " + str(ast))
