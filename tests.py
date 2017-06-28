from unittest import *
import unittest
from lambdacalculus import parse


## HOW TO RUN:
#  python -m unittest tests.TestsLambdaCalculus

class TestsLambdaCalculus(TestCase):

	# TODO: Add errors in each section....

	# Basic Nat operations

	def test_zero(self):
		self.assertEquals('0:Int',str(parse('0')))

	def test_succ_0(self): # succ(0) wins, Flawless victory
		self.assertEquals('succ(0):Nat',str(parse('succ(0)')))

	def test_pred_0(self):
		self.assertEquals('0:Nat',str(parse('pred(0)')))

	def test_pred_succ(self):
		self.assertEquals('0:Nat',str(parse('pred(succ(0))')))

	# Basic Bool operations

	def test_true(self):
		self.assertEquals('true:Bool',str(parse('true')))

	def test_false(self):
		self.assertEquals('false:Bool',str(parse('false')))

	#TODO: IF

	# Abstraction Tests

	def test_basic_abstraction_id_bool(self):
		self.assertEquals('\\x:Bool.x:Bool->Bool',str(parse('\\x:Bool.x')))

	def test_basic_abstraction_id_int(self):
		self.assertEquals('\\x:Int.x:Int->Int',str(parse('\\x:Int.x')))

	def test_basic_abstraction_id_arrow(self):
		self.assertEquals('\\x:Int->Bool.x:(Int->Bool)->(Int->Bool)',str(parse('\\x:Int->Bool.x')))

	def test_basic_abstraction_in_abstraction(self):
		self.assertEquals('\\x:Int.\\y:Bool.x:Int->Bool->Int',str(parse('\\x:Int.\\y:Bool.x')))


	# Application tests

	def test_id_application_int(self):
		self.assertEquals('0:Int',str(parse('\\x:Int.x 0')))

	def test_id_application_bool(self):
		self.assertEquals('false:Bool',str(parse('\\x:Bool.x false')))

	def test_application_repeated_variable_partial_application(self):
		self.assertEquals('\\x:Nat.succ(x):Nat->Nat',str(parse('\\x:Nat.\\xNat.succ(x) 0')))

	def test_application_repeated_variable_total_application(self):
		self.assertEquals('0:Nat',str(parse('\\x:Nat.\\xNat.succ(x) succ(0) 0')))
