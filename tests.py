from unittest import *
import unittest
from lambdacalculus import parse

def str_parse(input):
    return parse(input).str_with_type()
## HOW TO RUN:
#  python -m unittest tests.TestsLambdaCalculus

class TestsLambdaCalculus(TestCase):

    # TODO: Add errors in each section....

    # Basic Nat operations

    def test_zero(self):
        self.assertEquals('0:Nat',str_parse('0'))

    def test_succ_0(self): # succ(0) wins, Flawless victory
        self.assertEquals('succ(0):Nat',str_parse('succ(0)'))

    def test_pred_0(self):
        self.assertEquals('0:Nat',str_parse('pred(0)'))

    def test_pred_succ(self):
        self.assertEquals('0:Nat',str_parse('pred(succ(0))'))

	def test_multiple_succ_pred(self):
		self.assertEquals('0:Nat',str_parse('pred(pred(succ(succ(0))))'))

	# Basic Bool operations

    def test_true(self):
        self.assertEquals('true:Bool',str_parse('true'))

	def test_false(self):
		self.assertEquals('false:Bool',str_parse('false'))
        # IsZero Tests

    def test_is_zero_zero(self):
        self.assertEquals('true:Bool',str_parse('iszero(0)'))

    def test_is_one_zero(self):
        self.assertEquals('false:Bool',str_parse('iszero(succ(0))'))

    def test_is_pred_one_zero(self):
        self.assertEquals('true:Bool',str_parse('iszero(pred(succ(0)))'))

    def test_is_zero_succ_var(self):
        self.assertEquals('false:Bool', str_parse('iszero(succ(x))'))

    # IfThenElse Tests

    def test_if_then_else_true_condition(self):
        self.assertEquals('0:Nat',str_parse('if true then 0 else succ(0)'))

    def test_if_then_else_false_condition(self):
        self.assertEquals('succ(0):Nat',str_parse('if false then 0 else succ(0)'))

    def test_if_then_else_in_abstraction(self):
         self.assertEquals('\\x:Bool.if x then 0 else succ(0):Bool->Nat', str_parse('\\x:Bool.if x then 0 else succ(0)'))


    # Abstraction Tests

    def test_basic_abstraction_id_bool(self):
        self.assertEquals('\\x:Bool.x:Bool->Bool',str_parse('\\x:Bool.x'))

    def test_basic_abstraction_id_int(self):
        self.assertEquals('\\x:Nat.x:Nat->Nat',str_parse('\\x:Nat.x'))

    def test_basic_abstraction_id_arrow(self):
        self.assertEquals('\\x:Nat->Bool.x:(Nat->Bool)->(Nat->Bool)',str_parse('\\x:Nat->Bool.x'))

    def test_basic_abstraction_in_abstraction(self):
        self.assertEquals('\\x:Nat.\\y:Bool.x:Nat->Bool->Nat',str_parse('\\x:Nat.\\y:Bool.x'))


    # Application tests

    def test_id_application_int(self):
        self.assertEquals('0:Nat',str_parse('(\\x:Nat.x) 0'))

    def test_id_application_bool(self):
        self.assertEquals('false:Bool',str_parse('(\\x:Bool.x) false'))

    def test_application_repeated_variable_partial_application(self):
        self.assertEquals('\\x:Nat.succ(x):Nat->Nat',str_parse('(\\x:Nat.\\xNat.succ(x)) 0'))

    def test_application_repeated_variable_total_application(self):
        self.assertEquals('0:Nat',str_parse('(\\x:Nat.\\xNat.succ(x)) succ(0) 0'))
