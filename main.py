from lambdacalculus import lexer

while True:
    try:
        exp_str = raw_input('labdacalculus> ')
    except EOFError:
        break
    print(lexer.apply_lexer(exp_str))
