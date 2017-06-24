__all__ = ["Expression", "Natural", "Bool", "Abstraction", "Variable", "Succ"]

class Expression(object):

    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

    def e_type(self):
        return self._e_type

    def __str__(self):
        return str(self._value)

class Natural(Expression):

    def __init__(self, value):
        super(Natural,self).__init__(value)

    def pred(self):
        return Natural(max(self._value - 1, 0))

    def iszero(self):
        return Bool(self._value == 0)

class Bool(Expression):

    def __init__(self, value):
        super(Bool,self).__init__(value)

    def ifelse(self, expr_if_true, expr_if_false):
        return expr_if_true if self._value else expr_if_false

class Abstraction(Expression):

    def __init__(self, value):
        super(Bool,self).__init__(value)

class Variable(Expression):

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

    def substitute(self, varName, exp):
        return exp if varName == self._name else self

class Succ(Expression):
    def __init__(self, subexp):
        self._subexp = subexp

    def __str__(self):
        return "succ(" + str(self._subexp) + ")"

    def substitute(self, varName, exp):
        return Succ(self._subexp.substitute(varName,exp))
