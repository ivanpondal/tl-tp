__all__ = ["Expression", "Zero", "Bool", "Abstraction", "Variable", "Succ"]

Nat = 'Nat'

class Expression(object):

    def __init__(self, value):
        self._value = value
        self._type = "NoType"

    def value(self):
        return self._value

    def e_type(self):
        return self._e_type

    def __str__(self):
        return str(self._value)

    def strWithType(self):
        return str(self) + ":" + str(self._type)

class Bool(Expression):

    def __init__(self, value):
        super(Bool,self).__init__(value)

    def ifelse(self, expr_if_true, expr_if_false):
        return expr_if_true if self._value else expr_if_false

    def reduce(self):
        return self

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

class Zero(Expression):
    def __init__(self):
        self._type = Nat

    def __str__(self):
        return "0"

    def succAndReduce(self):
        # Precondition: self represents "0".
        # So succ operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Succ(self)

    def predAndReduce(self):
        # Precondition: self represents "0".
        # So pred operation should make no change.
        # Poscondition: I return "0".
        return self

class Succ(Expression):
    def __init__(self, subexp):
        self._subexp = subexp
        self._type = Nat

    def __str__(self):
        return "succ(" + str(self._subexp) + ")"

    def substitute(self, varName, exp):
        return Succ(self._subexp.substitute(varName,exp))

    def succAndReduce(self):
        # Precondition: self represents "succ(E)", reduced.
        # So succ operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Succ(self)

    def predAndReduce(self):
        # Precondition: self represents "succ(E)", reduced.
        # then doing pred(succ(E)) => E
        # Poscondition: I return the subexpression tree, therefore reduced
        return self._subexp

class Pred(Expression):
    def __init__(self, subexp):
        self._subexp = subexp
        self._type = Nat

    def __str__(self):
        return "pred(" + str(self._subexp) + ")"

    def substitute(self, varName, exp):
        return Pred(self._subexp.substitute(varName,exp))

    def reduce(self):
        return self._subexp.pred()

    def succAndReduce(self):
        # Precondition: self represents "pred(E)", reduced.
        # Then doing succ(pred(E)) => E
        # Postcondition: I return the subexpression tree, therefore reduced.
        return self._subexp

class IsZero(Expression):
    def __init__(self, subexp):
        self._subexp = subexp

    def __str__(self):
        return "iszero(" + str(self._subexp) + ")"

    def substitute(self, varName, exp):
        return IsZero(self._subexp.substitute(varName,exp))

    def reduce(self):
        return self._subexp.iszero()

class IfThenElse(Expression):
    def __init__(self, condition, value_if_true, value_if_false):
        self._condition = condition
        self._value_if_true = value_if_true
        self._value_if_false = value_if_false

    def __str__(self):
        return "if " + str(self._condition) + " then " + \
                str(self._value_if_true) + " else " + \
                str(self._value_if_false)

    def substitute(self, varName, exp):
        return IfThenElse(self._condition.substitute(varName, exp),
                          self._value_if_true.substitute(varName, exp),
                          self._value_if_false.substitue(varName, exp))

    def reduce(self):
        return self._condition.ifelse(self._value_if_true, self._value_if_false)


