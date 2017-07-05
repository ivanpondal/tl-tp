#! /usr/bin/env python
#! coding: utf-8

from __future__ import print_function
from lambdacalculus import parser, LambdaError
import sys, readline, optparse


usage = "usage: %prog [options] [expression]"

opt_parser = optparse.OptionParser(usage=usage)
opt_parser.add_option("-i", "--interactive", dest="interactive",
                      action="store_true", default=False,
                      help="use interactive prompt")

options, args = opt_parser.parse_args()


def input_exp(prompt="", exit_command=False):
    try:
        exp_str = raw_input(prompt)
    except EOFError:
        return False
    return exp_str if not exit_command or exp_str != exit_command else False


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
        if exp_str:
            parse_and_print(exp_str)
        else:
            break
else:
    exp_str = sys.argv[1] if len(sys.argv) > 1 else input_exp()
    status = parse_and_print(exp_str)
    if status:
        exit(0)
    else:
        exit(1)
