from lambdacalculus import parser

while True:
    try:
        exp_str = raw_input('labdacalculus> ')
    except EOFError:
        break
    value = parser.apply_parser(exp_str)
    print(value.strWithType())
