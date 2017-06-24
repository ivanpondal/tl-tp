from lambdacalculus import parser

while True:
    try:
        exp_str = raw_input('labdacalculus> ')
    except EOFError:
        break
    print(parser.apply_parser(exp_str))
