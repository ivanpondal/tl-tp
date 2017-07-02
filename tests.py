from unittest import *
import unittest
from lambdacalculus import parse, LambdaError


def str_parse(input):
    try:
        return parse(input).str_with_type()
    except LambdaError as e:
        return str(e)
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

    def test_numeral_as_multiple_succ(self):
        self.assertEquals('succ(succ(succ(succ(0)))):Nat', str_parse('4'))

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
        self.assertEquals('\\x:Nat->Bool.x:(Nat->Bool)->Nat->Bool',str_parse('\\x:Nat->Bool.x'))

    def test_basic_abstraction_in_abstraction(self):
        self.assertEquals('\\x:Nat.\\y:Bool.x:Nat->Bool->Nat',str_parse('\\x:Nat.\\y:Bool.x'))

    # Application tests

    def test_id_application_int(self):
        self.assertEquals('0:Nat',str_parse('(\\x:Nat.x) 0'))

    def test_id_application_bool(self):
        self.assertEquals('false:Bool',str_parse('(\\x:Bool.x) false'))

    def test_application_repeated_variable_partial_application(self):
        self.assertEquals('\\x:Nat.succ(x):Nat->Nat',str_parse('(\\x:Nat.\\x:Nat.succ(x)) 0'))

    def test_application_repeated_variable_total_application(self):
        self.assertEquals('succ(0):Nat', str_parse('((\\x:Nat.\\x:Nat.succ(x)) succ(0)) 0'))

    def test_application_successive(self):
        self.assertEquals('0:Nat', str_parse('(\\x:Nat.\\y:Nat.pred(y)) succ(0) 0'))

    def test_application_in_abstraction(self):
        self.assertEquals('\\f:Nat->Nat.\\x:Nat.f x:(Nat->Nat)->Nat->Nat', str_parse('\\f:Nat->Nat.\\x:Nat.f x'))

    def test_application_in_applied_abstraction(self):
        self.assertEquals('\\x:Nat.x:Nat->Nat', str_parse('(\\f:Nat->Nat.\\x:Nat.f x) \\x:Nat.x'))

    def test_application_with_variables(self):
        self.assertEquals('succ(0):Nat', str_parse('(\\x:Nat->Nat.\\y:Nat.x y) (\\z:Nat.succ(z)) 0'))

    # Free Term tests

    def test_evaluates_until_non_closed_term(self):
        # TODO: See what happens with this test after reviewing grammar
        self.assertEquals('ERROR: Non-closed term (y, x are free)',str_parse('(\\z:Nat.pred(succ(z))) \\x:Nat.y x'))

    # Examples provided in the task assignment

    def test_example_0(self):
        self.assertEquals('0:Nat',str_parse('0'))

    def test_example_true(self):
        self.assertEquals('true:Bool',str_parse('true'))

    def test_example_error_if_type(self):
        self.assertEquals('ERROR: Both if options should have the same type',\
            str_parse('if true then 0 else false'))

    def test_example_abstraction_if(self):
        self.assertEquals('\\x:Bool.if x then false else true:Bool->Bool',\
            str_parse('\\x:Bool.if x then false else true'))

    def test_example_abstraction_succ(self):
        self.assertEquals('\\x:Nat.succ(0):Nat->Nat',str_parse('\\x:Nat.succ(0)'))

    def test_example_print_abstraction(self):   
        self.assertEquals('\\z:Nat.z:Nat->Nat',str_parse('\\z:Nat.z'))

    def test_example_abstraction_type_application(self):   
        self.assertEquals('ERROR: succ expects a value of type Nat',str_parse('\\x:Bool.succ(x)) true'))

    def test_example_typing_nat(self):   
        self.assertEquals('succ(succ(succ(0))):Nat',str_parse('succ(succ(succ(0)))'))

    def test_example_error_free_var(self):   
        self.assertEquals('ERROR: Non-closed term (x is free)',str_parse('x'))

    def test_example_reduction_succ_pred(self):   
        self.assertEquals('succ(succ(0)):Nat',str_parse('succ(succ(pred(0)))'))

    def test_example_typing_abstraction(self):   
        self.assertEquals('\\x:Nat.succ(x):Nat->Nat',str_parse('\\x:Nat.succ(x)'))

    def test_example_error_not_a_function(self):   
        self.assertEquals('ERROR: Left part of application (0) is not a function of domain Nat',\
            str_parse('0 0'))

    def test_example_typing_multiple_abstraction(self):   
        self.assertEquals('\\x:Nat->Nat.\\y:Nat.\\z:Bool.if z then x y else 0:(Nat->Nat)->Nat->Bool->Nat',\
            str_parse('\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)'))

    def test_example_applying_multiple_abstraction(self):   
        self.assertEquals('succ(succ(succ(succ(succ(succ(succ(succ(succ(0))))))))):Nat',\
            str_parse('(\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)) (\\j:Nat.succ(j)) 8 true'))