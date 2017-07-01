from lambdacalculus import parser
import readline

while True:
    try:
        exp_str = raw_input('labdacalculus> ')
    except EOFError:
        break
    value = parser.apply_parser(exp_str)
    print(value.str_with_type())
