#! coding: utf-8

from . import LambdaError
from exp_type import *

__all__ = ["Expression", "Zero", "BoolExp", "Abstraction", "Variable", "Succ"]


class Expression(object):
    def __init__(self):
        self._free_vars = set()

    def free_vars(self):
        return self._free_vars

    def type(self):
        return self._type

    def str_with_type(self):
        if len(self._free_vars) > 0:
            raise LambdaNonClosedTermError("ERROR: Non-closed term ("
                + ", ".join(self._free_vars)
                + (" is" if len(self._free_vars) == 1 else " are") + " free)")
        return str(self) + ":" + str(self._type)

    def if_else(self, if_true_expr, if_false_expr):
        raise LambdaTypeError("ERROR: if condition should be of type Bool")

    def succ(self):
        raise LambdaTypeError("ERROR: succ expects a value of type Nat")

    def pred(self):
        raise LambdaTypeError("ERROR: pred expects a value of type Nat")

    def is_zero(self):
        raise LambdaTypeError("ERROR: iszero expects a value of type Nat")

    def apply(self,expr):
        raise LambdaTypeError("ERROR: Left part of application (" +\
        str(self) + ") is not a function of domain "+ \
        str(expr.type()))


class BoolExp(Expression):
    def __init__(self, value):
        super(BoolExp, self).__init__()
        self._value = value
        self._type = BoolType()

    def if_else(self, if_true_expr, if_false_expr):
        try:
            if_true_expr.type().unify_with(if_false_expr.type())
            return if_true_expr if self._value else if_false_expr
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: Both if options should have the same type")

    def substitute(self, var_name, expr):
        return self

    def __str__(self):
        return str(self._value).lower()


class Abstraction(Expression):
    def __init__(self, var, arg_type, body_expr):
        super(Abstraction, self).__init__()
        self._free_vars = body_expr.free_vars() - {str(var)}
        self._var = Variable(str(var), arg_type)
        self._body_expr = body_expr.substitute(str(var), self._var)
        self._type = AbstractionType(var_type=arg_type,
                                     body_type=body_expr.type(),
                                     var_name=str(var))


    def apply(self, expr_arg):
        try:
            expr_arg.type().unify_with(self._var.type())
            return self._body_expr.substitute(str(self._var), expr_arg)
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: left part of application is not a function with range " + str(expr_arg.type()))

    def __str__(self):
        return '\\' + str(self._var) + ':' + str(self._var.type()) + '.' + str(self._body_expr)

    def substitute(self, var_name, expr):
        return self if var_name == str(self._var) else \
            Abstraction(self._var, self._var.type(), self._body_expr.substitute(var_name, expr))


class Application(Expression):
    def __init__(self, left_expr, right_expr):
        super(Application, self).__init__()
        self._free_vars = left_expr.free_vars() | right_expr.free_vars()
        self._left_expr = left_expr
        self._right_expr = right_expr
        try:
            self._type = left_expr.type().body_type().unify_with(right_expr.type())
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: left part of application is not a function with range " + str(right_expr.type()))

    def __str__(self):
        return str(self._left_expr) + " " + str(self._right_expr)

    def substitute(self, var_name, expr):
        return self._left_expr.substitute(var_name, expr)\
            .apply(self._right_expr.substitute(var_name, expr))


class Variable(Expression):
    def __init__(self, name, var_type=None):
        super(Variable, self).__init__()
        self._free_vars.add(name)
        self._name = name
        self._type = TypeVar(name) if var_type == None else var_type

    def __str__(self):
        return self._name

    def substitute(self, var_name, expr):
        return expr if var_name == self._name else self

    def succ(self):
        try:
            self._type.unify_with(NatType())
            return Succ(self)
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: succ expects a value of type Nat")

    def pred(self):
        try:
            self._type.unify_with(NatType())
            return Pred(self)
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: pred expects a value of type Nat")

    def is_zero(self):
        try:
            self._type.unify_with(NatType())
            return IsZero(self)
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: iszero expects a value of type Nat")

    def if_else(self, if_true_expr, if_false_expr):
        # Precondition: self is a variable, it could be anything.
        # So if someone does if var then .... We need to construct the expression tree
        try:
            self._type.unify_with(BoolType())
            return IfThenElse(self, if_true_expr, if_false_expr)
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: if condition should be of type Bool")

    def apply(self, expr):
        try:
            self._type.unify_with(AbstractionType(expr.type(), TypeVar()))
            return Application(self, expr)
        except LambdaUnificationError:
            raise LambdaTypeError("ERROR: left part of application is not a function with range " + str(expr.type()))


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
        return self._sub_expr.substitute(var_name, expr).succ()

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
        return self._sub_expr.substitute(var_name, exp).pred()

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
        self._type = BoolType()

    def __str__(self):
        return "iszero(" + str(self._sub_expr) + ")"

    def substitute(self, var_name, exp):
        return self._sub_expr.substitute(var_name, exp).is_zero()

    def if_else(self, if_true_expr, if_false_expr):
        return IfThenElse(self, if_true_expr, if_false_expr)


class IfThenElse(Expression):
    def __init__(self, condition, if_true_expr, if_false_expr):
        super(IfThenElse, self).__init__()
        self._free_vars = condition.free_vars() | if_true_expr.free_vars() | if_false_expr.free_vars()
        self._condition = condition
        self._if_true_expr = if_true_expr
        self._if_false_expr = if_false_expr
        try:
            self._type = if_true_expr.type().unify_with(if_false_expr.type())
        except LambdaUnificationError():
            raise LambdaTypeError("ERROR: Both if options should have the same type")

    def __str__(self):
        return "if " + str(self._condition) + " then " + \
               str(self._if_true_expr) + " else " + \
               str(self._if_false_expr)

    def substitute(self, var_name, exp):
        return self._condition.substitute(var_name, exp).if_else(
            self._if_true_expr.substitute(var_name, exp),
            self._if_false_expr.substitute(var_name, exp))

    def if_else(self, if_true_expr, if_false_expr):
        return self


class LambdaTypeError(LambdaError):
    pass

class LambdaNonClosedTermError(LambdaError):
    pass
