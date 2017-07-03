#! coding: utf-8

from __future__ import print_function
from lambdacalculus import parser, LambdaError
import readline, sys

while True:
    try:
        exp_str = raw_input('λ> ')
    except EOFError:
        break
    try:
        value = parser.apply_parser(exp_str)
        print(value.str_with_type())
    except LambdaError as e:
        print(e, file=sys.stderr)
