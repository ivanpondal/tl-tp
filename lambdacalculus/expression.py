from sets import Set
from exp_type import *

__all__ = ["Expression", "Zero", "BoolExp", "Abstraction", "Variable", "Succ"]


class Expression(object):

    def __init__(self):
        self._type = "NoType"
        self._free_vars = Set([])

    def free_vars(self):
        return self._free_vars

    def e_type(self):
        return self._e_type

    def str_with_type(self):
        return str(self) + ":" + str(self._type)

class BoolExp(Expression):

    def __init__(self, value):
        super(BoolExp, self).__init__()
        self._value = value
        self._type = BoolType()

    def if_else(self, expr_if_true, expr_if_false):
        return expr_if_true if self._value else expr_if_false

    def __str__(self):
        return str(self._value).lower()


class Abstraction(Expression):

    def __init__(self, var, arg_type, expr_body):
        super(Abstraction, self).__init__()
        self._free_vars = expr_body.free_vars() - Set([str(var)])
        self._var = var
        self._arg_type = arg_type
        self._expr_body = expr_body

    def apply(self, expr_arg):
        return self._expr_body.substitute(str(self._var), expr_arg)

    def __str__(self):
        return '\\' + str(self._var) + '.' + str(self._arg_type) + ':' + str(self._expr_body)

class Variable(Expression):

    def __init__(self, name):
        super(Variable, self).__init__()
        self._free_vars.add(name)
        self._name = name

    def __str__(self):
        return self._name

    def substitute(self, var_name, expr):
        return expr if var_name == self._name else self

    def succ(self):
        return Succ(self)

    def if_else(self, expr_if_true, expr_if_false):
        # TODO: Blow Up if type is not correct
        # Precondition: self is a variable, it could be anything.
        # So if someone does if var then .... We need to construct the expression tree
        return IfThenElse(self, expr_if_true, expr_if_false)

class Zero(Expression):
    def __init__(self):
        super(Zero, self).__init__()
        self._type = NatType()

    def __str__(self):
        return "0"

    def substitute(self, var_name, expr):
        return self

    def succ(self):
        # Precondition: self represents "0".
        # So succ operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Succ(self)

    def pred(self):
        # Precondition: self represents "0".
        # So pred operation should make no change.
        # Poscondition: I return "0".
        return self

    def is_zero(self):
        # Precondition: self represents "0"
        # so i'm zero.
        return BoolExp(True)

class Succ(Expression):
    def __init__(self, subexp):
        super(Succ,self).__init__()
        self._free_vars = subexp.free_vars()
        self._subexp = subexp
        self._type = NatType()

    def __str__(self):
        return "succ(" + str(self._subexp) + ")"

    def substitute(self, var_name, exp):
        return Succ(self._subexp.substitute(var_name,exp))

    def succ(self):
        # Precondition: self represents "succ(E)", reduced.
        # So succ operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Succ(self)

    def pred(self):
        # Precondition: self represents "succ(E)", reduced.
        # then doing pred(succ(E)) => E
        # Poscondition: I return the subexpression tree, therefore reduced
        return self._subexp

    def is_zero(self):
        # Precondition: self represents "succ(E)", reduced.
        # so if someone asks if I'm zero, I depend on the free vars.
        return BoolExp(False)

class Pred(Expression):
    def __init__(self, subexp):
        super(Pred, self).__init__()
        self._free_vars = subexp.free_vars()
        self._subexp = subexp
        self._type = NatType()

    def __str__(self):
        return "pred(" + str(self._subexp) + ")"

    def substitute(self, var_name, exp):
        return Pred(self._subexp.substitute(var_name,exp))

    def succ(self):
        # Precondition: self represents "pred(E)", reduced.
        # Then doing succ(pred(E)) => E
        # Postcondition: I return the subexpression tree, therefore reduced.
        return self._subexp

    def pred(self):
        # Precondition: self represents "pred(E)", reduced.
        # So pred operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Pred(self)

    def is_zero(self):
        # Precondition: self represents "pred(E)", reduced.
        # so if someone asks if I'm zero, I need to evaluate completely.
        # My only choice is to grow the expression tree:
        return IsZero(self)

class IsZero(Expression):
    def __init__(self, subexp):
        super(IsZero,self).__init__()
        self._free_vars = subexp.free_vars()
        self._subexp = subexp

    def __str__(self):
        return "iszero(" + str(self._subexp) + ")"

    def substitute(self, var_name, exp):
        return IsZero(self._subexp.substitute(var_name,exp))

class IfThenElse(Expression):

    def __init__(self, condition, expr_if_true, expr_if_false):
        super(IfThenElse, self).__init__()
        self._free_vars = condition.free_vars() | expr_if_true.free_vars() | expr_if_false.free_vars()
        self._condition = condition
        self._expr_if_true = expr_if_true
        self._expr_if_false = expr_if_false

    def __str__(self):
        return "if " + str(self._condition) + " then " + \
                str(self._expr_if_true) + " else " + \
                str(self._expr_if_false)

    def substitute(self, var_name, exp):
        return IfThenElse(self._condition.substitute(var_name, exp),
                          self._expr_if_true.substitute(var_name, exp),
                          self._expr_if_false.substitue(var_name, exp))

    def if_else(self, expr_if_true, expr_if_false):
        return self