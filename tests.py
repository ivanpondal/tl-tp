from unittest import *
import unittest
from lambdacalculus import parse

def strParse(input):
	return parse(input).strWithType()
## HOW TO RUN:
#  python -m unittest tests.TestsLambdaCalculus

class TestsLambdaCalculus(TestCase):

	# TODO: Add errors in each section....

	# Basic Nat operations

	def test_zero(self):
		self.assertEquals('0:Nat',strParse('0'))

	def test_succ_0(self): # succ(0) wins, Flawless victory
		self.assertEquals('succ(0):Nat',strParse('succ(0)'))

	def test_pred_0(self):
		self.assertEquals('0:Nat',strParse('pred(0)'))

	def test_pred_succ(self):
		self.assertEquals('0:Nat',strParse('pred(succ(0))'))

	# Basic Bool operations

	def test_true(self):
		self.assertEquals('true:Bool',strParse('true'))

	def test_false(self):
		self.assertEquals('false:Bool',strParse('false'))

	#TODO: IF

	# Abstraction Tests

	def test_basic_abstraction_id_bool(self):
		self.assertEquals('\\x:Bool.x:Bool->Bool',strParse('\\x:Bool.x'))

	def test_basic_abstraction_id_int(self):
		self.assertEquals('\\x:Nat.x:Nat->Nat',strParse('\\x:Nat.x'))

	def test_basic_abstraction_id_arrow(self):
		self.assertEquals('\\x:Nat->Bool.x:(Nat->Bool)->(Nat->Bool)',strParse('\\x:Nat->Bool.x'))

	def test_basic_abstraction_in_abstraction(self):
		self.assertEquals('\\x:Nat.\\y:Bool.x:Nat->Bool->Nat',strParse('\\x:Nat.\\y:Bool.x'))


	# Application tests

	def test_id_application_int(self):
		self.assertEquals('0:Nat',strParse('\\x:Nat.x 0'))

	def test_id_application_bool(self):
		self.assertEquals('false:Bool',strParse('\\x:Bool.x false'))

	def test_application_repeated_variable_partial_application(self):
		self.assertEquals('\\x:Nat.succ(x):Nat->Nat',strParse('\\x:Nat.\\xNat.succ(x) 0'))

	def test_application_repeated_variable_total_application(self):
		self.assertEquals('0:Nat',strParse('\\x:Nat.\\xNat.succ(x) succ(0) 0'))
