from . import LambdaError

__all__ = ["BoolType",
           "NatType",
           "AbstractionType",
           "TypeVar",
           "NamedTypeVar",
           "LambdaUnificationError"]


class LambdaUnificationError(LambdaError):
    pass


class ExpType(object):

    def unify_with_bool(self):
        raise LambdaUnificationError("ERROR: Types " + str(self) +
                                     " and Bool do not unify")

    def unify_with_nat(self):
        raise LambdaUnificationError("ERROR: Types " + str(self) +
                                     " and Nat do not unify")

    def unify_with_abstraction(self, an_abstraction):
        raise LambdaUnificationError("ERROR: Types " + str(self) + " and " +
                                     str(an_abstraction) + " do not unify")


class BoolType(ExpType):

    def __str__(self):
        return 'Bool'

    def str_assoc(self):
        return str(self)

    def bind(self, name, type):
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

    def bind(self, name, type):
        return self

    def unify_with(self, other_type):
        return other_type.unify_with_nat()

    def unify_with_nat(self):
        return self


class AbstractionType(ExpType):

    def __init__(self, arg_type, body_type, arg_name=None):
        self._arg_name = arg_name
        self._arg_type = arg_type
        self._body_type = body_type.bind(arg_name, arg_type)

    def __str__(self):
        return self._arg_type.str_assoc() + '->' + str(self._body_type)

    def str_assoc(self):
        return '(' + str(self) + ')'

    def var_type(self):
        return self._arg_type

    def body_type(self):
        return self._body_type

    def bind(self, name, type):
        return self if name == self._arg_name else \
            AbstractionType(self._arg_type,
                            self._body_type.bind(name, type),
                            self._arg_name)

    def unify_with(self, other_type):
        return other_type.unify_with_abstraction(self)

    def unify_with_abstraction(self, an_abstraction):
        return AbstractionType(
            self._arg_type.unify_with(an_abstraction.var_type()),
            self._body_type.unify_with(an_abstraction.body_type()))


class TypeVar(ExpType):

    def __init__(self, name=None):
        pass

    def __str__(self):
        return 'AnyType'

    def str_assoc(self):
        return str(self)

    def var_type(self):
        return TypeVar()

    def body_type(self):
        return TypeVar()

    def bind(self, name, type):
        return self

    def unify_with(self, other_type):
        return other_type

    def unify_with_bool(self):
        return BoolType()

    def unify_with_nat(self):
        return NatType()

    def unify_with_abstraction(self, an_abstraction):
        return an_abstraction


class NamedTypeVar(TypeVar):

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return 'AnyType[' + self._name + ']'

    def bind(self, name, type):
        return type if self._name == name else self

