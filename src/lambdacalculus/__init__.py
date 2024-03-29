#! coding: utf-8

class LambdaError(Exception):
    pass

from .lexer import apply_lexer as lex
from .parser import apply_parser as parse
