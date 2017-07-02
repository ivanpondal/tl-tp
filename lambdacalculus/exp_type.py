from . import LambdaError

__all__ = ["BoolType",
           "NatType",
           "AbstractionType",
           "TypeVar",
           "LambdaUnificationError"]


class LambdaUnificationError(LambdaError):
    pass


class ExpType(object):

    def unify_with_bool(self):
        raise LambdaUnificationError("ERROR: Types " + str(self) + " and Bool do not unify")

    def unify_with_nat(self):
        raise LambdaUnificationError("ERROR: Types " + str(self) + " and Nat do not unify")

    def unify_with_abstraction(self, other_abs):
        raise LambdaUnificationError("ERROR: Types " + str(self) + " and " + str(other_abs) + " do not unify")


class BoolType(ExpType):

    def __str__(self):
        return 'Bool'

    def str_assoc(self):
        return str(self)

    def substitute(self, name, type):
        return self

    def unify_with(self, other_type):
        return other_type.unify_with_bool()

    def unify_with_bool(self):
        return self


class NatType(ExpType):

    def __str__(self):
        return 'Nat'

    def str_assoc(self):
        return str(self)

    def substitute(self, name, type):
        return self

    def unify_with(self, other_type):
        return other_type.unify_with_nat()

    def unify_with_nat(self):
        return self


class AbstractionType(ExpType):

    def __init__(self, var_type, body_type, var_name=None):
        self._var_name = var_name
        self._var_type = var_type
        self._body_type = body_type.substitute(var_name, var_type)

    def __str__(self):
        return self._var_type.str_assoc() + '->' + str(self._body_type)

    def str_assoc(self):
        return '(' + str(self) + ')'

    def var_type(self):
        return self._var_type

    def body_type(self):
        return self._body_type

    def substitute(self, name, type):
        return self if name == self._var_name else \
            AbstractionType(self._var_type,
                            self._body_type.substitute(name, type),
                            self._var_name)

    def unify_with(self, other_type):
        return other_type.unify_with_abstraction(self)

    def unify_with_abstraction(self, other_abs):
        return AbstractionType(self._var_type.unify_with(other_abs.var_type()),
                               self._body_type.unify_with(other_abs.body_type()),
                               self._var_name)


class TypeVar(ExpType):

    def __init__(self, name=None):
        self._name = name

    def __str__(self):
        return 'AnyType'

    def str_assoc(self):
        return str(self)

    def var_type(self):
        return TypeVar()

    def body_type(self):
        return TypeVar()

    def substitute(self, name, type):
        return type if self._name == name else self

    def unify_with(self, other_type):
        return other_type

    def unify_with_bool(self):
        return BoolType()

    def unify_with_nat(self):
        return NatType()

    def unify_with_abstraction(self, other_abs):
        return other_abs



