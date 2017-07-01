__all__ = ["BoolType", "NatType", "AbstractionType", "TypeVar"]

class ExpType(object):
    pass

class BoolType(ExpType):

    def __str__(self):
        return 'Bool'

    def str_assoc(self):
        return str(self)

    def substitute(self, name, type):
        return self

class NatType(ExpType):

    def __str__(self):
        return 'Nat'

    def str_assoc(self):
        return str(self)

    def substitute(self, name, type):
        return self

class AbstractionType(ExpType):

    def __init__(self, arg_name, arg_type, body_type):
        self._arg_name = arg_name
        self._arg_type = arg_type
        self._body_type = body_type.substitute(arg_name, arg_type)

    def __str__(self):
        return str(self._arg_type) + '->' + self._body_type.str_assoc()

    def str_assoc(self):
        return '(' + str(self) + ')'

    def substitute(self, name, type):
        return self if name == self._arg_name else \
            AbstractionType(self._arg_name, self._arg_type,
                            self._body_type.substitute(name, type))

class TypeVar(ExpType):

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return 'AnyType'

    def str_assoc(self):
        return str(self)

    def substitute(self, name, type):
        return type if self._name == name else self
