class Expression:

    def __init__(self, value, e_type):
        self._value = value
        self._e_type = e_type

    def value(self):
        return self._value

    def e_type(self):
        return self._e_type

    def __repr__(self):
        return str(self._value)

class Natural(Expression):

    def __init__(self, value):
        self._value = value
        self._e_type = 'nat'

    def succ(self):
       return Natural(self._value + 1)
