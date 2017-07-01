from sets import Set
from exp_type import *

__all__ = ["Expression", "Zero", "BoolExp", "Abstraction", "Variable", "Succ"]


class Expression(object):
    def __init__(self):
        self._type = "NoType"
        self._free_vars = Set([])

    def free_vars(self):
        return self._free_vars

    def type(self):
        return self._type

    def str_with_type(self):
        return str(self) + ":" + str(self._type)


class BoolExp(Expression):
    def __init__(self, value):
        super(BoolExp, self).__init__()
        self._value = value
        self._type = BoolType()

    def if_else(self, if_true_expr, if_false_expr):
        return if_true_expr if self._value else if_false_expr

    def __str__(self):
        return str(self._value).lower()


class Abstraction(Expression):
    def __init__(self, var, arg_type, body_expr):
        super(Abstraction, self).__init__()
        self._free_vars = body_expr.free_vars() - Set([str(var)])
        self._var = var
        self._arg_type = arg_type
        self._body_expr = body_expr

    def apply(self, expr_arg):
        return self._body_expr.substitute(str(self._var), expr_arg)

    def __str__(self):
        return '\\' + str(self._var) + '.' + str(self._arg_type) + ':' + str(self._body_expr)

    def substitute(self, var_name, expr):
        return self if var_name != str(self._var) else \
            Abstraction(self._var, self._arg_type, self._body_expr.substitute(var_name, expr))


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

    def if_else(self, if_true_expr, if_false_expr):
        # TODO: Blow Up if type is not correct
        # Precondition: self is a variable, it could be anything.
        # So if someone does if var then .... We need to construct the expression tree
        return IfThenElse(self, if_true_expr, if_false_expr)


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
    def __init__(self, sub_expr):
        super(Succ, self).__init__()
        self._free_vars = sub_expr.free_vars()
        self._sub_expr = sub_expr
        self._type = NatType()

    def __str__(self):
        return "succ(" + str(self._sub_expr) + ")"

    def substitute(self, var_name, expr):
        return Succ(self._sub_expr.substitute(var_name, expr))

    def succ(self):
        # Precondition: self represents "succ(E)", reduced.
        # So succ operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Succ(self)

    def pred(self):
        # Precondition: self represents "succ(E)", reduced.
        # then doing pred(succ(E)) => E
        # Poscondition: I return the subexpression tree, therefore reduced
        return self._sub_expr

    def is_zero(self):
        # Precondition: self represents "succ(E)", reduced.
        # so if someone asks if I'm zero, I depend on the free vars.
        return BoolExp(False)


class Pred(Expression):
    def __init__(self, sub_expr):
        super(Pred, self).__init__()
        self._free_vars = sub_expr.free_vars()
        self._sub_expr = sub_expr
        self._type = NatType()

    def __str__(self):
        return "pred(" + str(self._sub_expr) + ")"

    def substitute(self, var_name, exp):
        return Pred(self._sub_expr.substitute(var_name, exp))

    def succ(self):
        # Precondition: self represents "pred(E)", reduced.
        # Then doing succ(pred(E)) => E
        # Postcondition: I return the subexpression tree, therefore reduced.
        return self._sub_expr

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
    def __init__(self, sub_expr):
        super(IsZero, self).__init__()
        self._free_vars = sub_expr.free_vars()
        self._sub_expr = sub_expr

    def __str__(self):
        return "iszero(" + str(self._sub_expr) + ")"

    def substitute(self, var_name, exp):
        return IsZero(self._sub_expr.substitute(var_name, exp))


class IfThenElse(Expression):
    def __init__(self, condition, if_true_expr, if_false_expr):
        super(IfThenElse, self).__init__()
        self._free_vars = condition.free_vars() | if_true_expr.free_vars() | if_false_expr.free_vars()
        self._condition = condition
        self._if_true_expr = if_true_expr
        self._if_false_expr = if_false_expr

    def __str__(self):
        return "if " + str(self._condition) + " then " + \
               str(self._if_true_expr) + " else " + \
               str(self._if_false_expr)

    def substitute(self, var_name, exp):
        return IfThenElse(self._condition.substitute(var_name, exp),
                          self._if_true_expr.substitute(var_name, exp),
                          self._if_false_expr.substitue(var_name, exp))

    def if_else(self, if_true_expr, if_false_expr):
        return self
