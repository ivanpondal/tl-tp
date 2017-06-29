from sets import Set

__all__ = ["Expression", "Zero", "BoolExp", "Abstraction", "Variable", "Succ"]

tNat = 'Nat'
tBool = 'Bool'

class Expression(object):

    def __init__(self):
        self._type = "NoType"
        self._freeVars = Set([])

    def e_type(self):
        return self._e_type

    def __str__(self):
        return str(self._value)

    def strWithType(self):
        return str(self) + ":" + str(self._type)

class BoolExp(Expression):

    def __init__(self, value):
        super(BoolExp,self).__init__()
        self._value = value
        self._type = tBool

    def ifElseReduce(self, expr_if_true, expr_if_false):
        # Precondition: self represents either a true or a false, reduced, final.
        # so if someone does if self then .... I now have to reduce, and choose the subexpression.
        return expr_if_true if self._value else expr_if_false

    def __str__(self):
        return str(self._value).lower()


class Abstraction(Expression):

    def __init__(self, value):
        super(Abstraction,self).__init__()

class Variable(Expression):

    def __init__(self, name):
        super(Variable,self).__init__()
        self._name = name

    def __str__(self):
        return self._name

    def substitute(self, varName, exp):
        return exp if varName == self._name else self

    def ifElseReduce(self, expr_if_true, expr_if_false):
        # TODO: Blow Up if type is not correct
        # Precondition: self is a variable, it could be anything.
        # So if someone does if var then .... We need to construct the expression tree
        return IfThenElse(self, expr_if_true, expr_if_false)

class Zero(Expression):
    def __init__(self):
        super(Zero,self).__init__()
        self._type = tNat

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

    def isZero(self):
        # Precondition: self represents "0"
        # so i'm zero.
        return BoolExp(True)

class Succ(Expression):
    def __init__(self, subexp):
        super(Succ,self).__init__()
        self._subexp = subexp
        self._type = tNat

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

    def isZero(self):
        # Precondition: self represents "succ(E)", reduced.
        # so if someone asks if I'm zero, I depend on the free vars.
        return BoolExp(False) if len(self._freeVars) == 0 else IsZero(self)

class Pred(Expression):
    def __init__(self, subexp):
        super(Pred,self).__init__()
        self._subexp = subexp
        self._type = tNat

    def __str__(self):
        return "pred(" + str(self._subexp) + ")"

    def substitute(self, varName, exp):
        return Pred(self._subexp.substitute(varName,exp))

    def succAndReduce(self):
        # Precondition: self represents "pred(E)", reduced.
        # Then doing succ(pred(E)) => E
        # Postcondition: I return the subexpression tree, therefore reduced.
        return self._subexp

    def predAndReduce(self):
        # Precondition: self represents "pred(E)", reduced.
        # So pred operation should make the tree grow.
        # Poscondition: I return the new expression tree, also reduced.
        return Pred(self)

    def isZero(self):
        # Precondition: self represents "pred(E)", reduced.
        # so if someone asks if I'm zero, I need to evaluate completely.
        # My only choice is to grow the expression tree:
        return IsZero(self)

class IsZero(Expression):
    def __init__(self, subexp):
        super(IsZero,self).__init__()
        self._subexp = subexp

    def __str__(self):
        return "iszero(" + str(self._subexp) + ")"

    def substitute(self, varName, exp):
        return IsZero(self._subexp.substitute(varName,exp))

class IfThenElse(Expression):
    def __init__(self, condition, value_if_true, value_if_false):
        super(IfThenElse,self).__init__()
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


