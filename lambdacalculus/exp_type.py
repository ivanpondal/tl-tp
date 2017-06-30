__all__ = ["BoolType", "NatType"]

class ExpType(object):
	pass

class BoolType(ExpType):

    def __str__(self):
    	return 'Bool'

class NatType(ExpType):

    def __str__(self):
    	return 'Nat'