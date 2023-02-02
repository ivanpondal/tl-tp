#!/usr/bin/env python3

from lambdacalculus import parser, LambdaError
import sys, readline, optparse


usage = "usage: %prog [options] [expression]"

opt_parser = optparse.OptionParser(usage=usage)
opt_parser.add_option("-i", "--interactive", dest="interactive",
                      action="store_true", default=False,
                      help="use interactive prompt")

options, args = opt_parser.parse_args()


def input_exp(prompt="", exit_command=None):
    try:
        exp_str = input(prompt)
    except EOFError:
        return None
    return exp_str if exit_command is None or exp_str != exit_command else None


def parse_and_print(exp_str):
    try:
        value = parser.apply_parser(exp_str)
        print(value.str_with_type())
        return True
    except LambdaError as e:
        print(e, file=sys.stderr)
        return False


if options.interactive:
    while True:
        exp_str = input_exp(prompt="λ> ", exit_command=":q")
        if exp_str is not None:
            parse_and_print(exp_str)
        else:
            break
else:
    exp_str = sys.argv[1] if len(sys.argv) > 1 else input_exp()
    if exp_str is not None:
        status = parse_and_print(exp_str)
        if status:
            exit(0)
    exit(1)
