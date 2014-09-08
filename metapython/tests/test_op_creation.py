import unittest
import nose

from metaprogramming.op.Op import *
from metaprogramming.op.pandas_formatting import *
from metaprogramming.op.text_preprocessing import *
from metaprogramming.op.topic_modelling import *
from metaprogramming.op.print_utils import *
from metaprogramming.op.featurize import *


def series_equal(s1, s2, precision=2):
	"""
		given two series composed of floating point numbers,
		asserts that they are equal to 'precision' floating 
		point numbers
	"""
	return all(s1.round(precision) == s2.round(precision))

################################################################################
####################[ From Functions ]##########################################
################################################################################

class Test_from_function(unittest.TestCase):

	def setUp(self):
		pass

	def basic_test(self):
		@op(num_out=1)
		def square(x):
			return x**2
		self.assertEquals(square(2), 4)


	def test_add_1(self):
		@op(num_out=1)
		def square(x):
			return x**2
		x = (square + square)(2)
		self.assertEquals(x, 16)


	def test_add_2(self):
		@op(num_out=1)
		def square(x, scalar=None):
			return x**scalar
		@op(num_out=1)
		def add(x, scalar=None):
			return x*scalar

		x = (square + add)(2, scalar=2)
		self.assertEquals(x, 8)


	def test_args_1(self):
		@op(num_out=1)
		def square(x, scalar=None):
			return x**scalar
		x = (square + square)(2, scalar=2)
		self.assertEquals(x, 16)


	def test_args_2(self):
		@op(num_out=1)
		def square(x, scalar=None):
			return x**scalar
		x = (square + square)(scalar=2)(2)
		self.assertEquals(x, 16)


	def test_join_1(self):
		@op(num_out=1)
		def square(x):
			return x**2
		@op(num_out=1)
		def cube(x):
			return x**3
		joined = (square | cube)
		s, c = joined(2, 2)
		self.assertEquals(s, 4)
		self.assertEquals(c, 8)


	def test_join_2(self):
		@op(num_out=1)
		def double(x, scalar=None):
			return (x*scalar*scalar)
		@op(num_out=1)
		def tripple(x, scalar=None):
			return (x*scalar*scalar*scalar)
		joined = (double | tripple)
		s, c = joined(2, 2, scalar=2)
		self.assertEquals(s, 8)
		self.assertEquals(c, 16)


	def test_join_add(self):
		@op(num_out=1)
		def square(x):
			return x**2
		@op(num_out=1)
		def cube(x):
			return x**3
		@op(num_out=1)
		def add(x,y):
			return x+y

		x = (split_op + (square | cube) + add)(2)
		self.assertEquals(x, 12)


	def test_join_add_args(self):
		@op(num_out=1)
		def square(x, scalar=None):
			return (x**2)*scalar
		@op(num_out=1)
		def cube(x, scalar=None):
			return (x**3)*scalar
		@op(num_out=1)
		def add(x,y):
			return x+y
		x = (split_op + (square | cube) + add)(2, scalar=2)
		self.assertEquals(x, 24)





# %%%%% FROM LAMBDAS %%%%%

class Test_from_lambdas(unittest.TestCase):

	def setUp(self):
		pass

	def test_single_operand(self):
		id_op = op(1, lambda x:x)
		self.assertTrue(id_op(1), 1)

	def test_multiple_input(self):
		add_op = op(1, lambda x,y: x+y)
		self.assertTrue(add_op(6,11),17)

	def test_multiple_output(self):
		split_op = op(2, lambda x:(x,x))
		self.assertTrue(split_op(5)[0], 5)
		self.assertTrue(split_op(5)[1], 5)

	def test_multiple_in_out(self):
		diffs = op(2, lambda x,y,z: (y-x, z-y))
		self.assertTrue(diffs(4,5,7)[0], 1)
		self.assertTrue(diffs(4,5,7)[1], 1)
		self.assertTrue(len(diffs(4,5,7)), 2)

	def test_string(self):
		lower_split = op(1, lambda s: s.lower().split())
		self.assertTrue(lower_split('ASD dS s'), ['asd', 'ds', 's'])



################################################################################
####################[ From Opscripts ]##########################################
################################################################################

def series_equal(s1, s2, precision=2):
	"""
		given two series composed of floating point numbers,
		asserts that they are equal to 'precision' floating 
		point numbers
	"""
	return all(s1.round(precision) == s2.round(precision))

class Test_from_opscript(unittest.TestCase):

	def setUp(self):
		pass


	def test_single_operand(self):
		op = FromOpScript ([
					(1, 1, 'lambda df: apply_and_store(df, ["a"], ["a+1"], lambda s: s+1)'),
					(1, 1, 'lambda df: apply_and_store(df, ["b"], ["b*2"], lambda s: s*2)'),
				])
		df = pd.DataFrame (np.random.randn(5, 2), columns=['a', 'b'])
		df = op(df)
		self.assertTrue(series_equal(df['a+1'], df['a']+1))
		self.assertTrue(series_equal(df['b*2'], df['b']*2))


	def test_single_operand_addition(self):
		op1 = FromOpScript([	(1, 1, 'lambda df: apply_and_store(df, ["a"], ["a+1"], lambda s: s+1)')])
		op2 = FromOpScript([	(1, 1, 'lambda df: apply_and_store(df, ["b"], ["b*2"], lambda s: s*2)')])
		df = pd.DataFrame(np.random.randn(5,2), columns=['a','b'])
		df = (op1 + op2)(df)
		self.assertTrue(series_equal(df['a+1'], df['a']+1))
		self.assertTrue(series_equal(df['b*2'], df['b']*2))


	def test_multiple_operands(self):
		op = FromOpScript([(3, 2, 'lambda x1,x2,x3: (x1["a"]+x2["c"]+x3["e"], x1["b"]*x2["d"]*x3["f"])')])
		df1 = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		df2 = pd.DataFrame (np.random.randn(10,2), columns=['c','d'])	
		df3 = pd.DataFrame (np.random.randn(10,2), columns=['e','f'])
		s, p = op(df1, df2, df3)
		self.assertTrue(series_equal(s, df1['a'] + df2['c'] + df3['e']))
		self.assertTrue(series_equal(p, df1['b'] * df2['d'] * df3['f']))


	def test_multiple_operands_addition(self):
		op1 = FromOpScript([(3, 2, 'lambda x1,x2,x3: (x1["a"]+x2["c"]+x3["e"], x1["b"]*x2["d"]*x3["f"])')])
		op2 = FromOpScript([(2, 1, 'lambda s,p: s+p')])
		df1 = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		df2 = pd.DataFrame (np.random.randn(10,2), columns=['c','d'])	
		df3 = pd.DataFrame (np.random.randn(10,2), columns=['e','f'])
		out = (op1 + op2)(df1, df2, df3)
		self.assertTrue(series_equal(out, (df1['a']+df2['c']+df3['e']) + (df1['b']*df2['d']*df3['f'])))


	def test_nop(self):
		nop = FromOpScript([(0, 0, "pass")])
		op = FromOpScript([(1, 1, 'lambda df: apply_and_store(df, ["a"], ["a+1"], lambda s: s+1)')])
		df = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		df = (nop + op + nop)(df)
		self.assertTrue(series_equal(df['a+1'], df['a']+1))


	def test_zero_input_one_output(self):
		op = FromOpScript([(0, 1, 'lambda: 2**2')])
		out = op()
		self.assertEquals(out, 2**2)


	def test_zero_input_two_outputs(self):
		op = FromOpScript([(0, 2, 'lambda: (2**2, 3**2)')])
		out = op()
		self.assertEquals(out[0], 2**2)
		self.assertEquals(out[1], 3**2)



	def test_join_num_in_num_out(self):		
		op1 = FromOpScript([(1, 1, 'lambda df: df["c"]')])
		op2 = FromOpScript([(1, 1, 'lambda df: df["e"]')])
		op3 = (op1 | op2)
		self.assertEquals(op3.num_in, 2)
		self.assertEquals(op3.num_out,2)


	def test_join_1(self):
		op1 = FromOpScript([(1, 1, 'lambda df: df["a"]')])
		op2 = FromOpScript([(1, 1, 'lambda df: df["b"]')])
		op3 = (op1 | op2)
		df1 = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		df2 = pd.DataFrame (np.random.randn(10,2), columns=['b','c'])
		o_0, o_1 = op3(df1, df2)
		self.assertTrue(series_equal(df1['a'], o_0))
		self.assertTrue(series_equal(df2['b'], o_1))	


	def test_join_2(self):
		op1 = FromOpScript([(1, 1, 'lambda df: df["c"]')])
		op2 = FromOpScript([(1, 1, 'lambda df: df["d"]')])
		op3 = FromOpScript([(2, 1, "lambda x1, x2: x1 + x2")])
		op4 = (op1 | op2) + op3
		df1 = pd.DataFrame (np.random.randn(10,2), columns=['c','d'])
		df2 = pd.DataFrame (np.random.randn(10,2), columns=['d','e'])
		out = op4(df1, df2)
		self.assertTrue(series_equal(df1['c'] + df2['d'], out))


	def test_join_add(self):
		op1 = FromOpScript([(1, 2, 'lambda df: (df["a"], df["b"])')])
		op2 = FromOpScript([(1, 1, 'lambda s: s+1')])
		op3 = FromOpScript([(1, 1, 'lambda s: s*2')])
		op4 = FromOpScript([(2, 1, "lambda x1, x2: x1 + x2")])
		op5 = op1 + (op2 | op3) + op4
		df = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		out = op5(df)
		self.assertTrue(series_equal(out, (df['a']+1)+(df['b']*2)))


	def test_args_basic(self):
		aop = FromOpScript([
					(1, 1, 'lambda df: apply_and_store(df, ["{col}"], ["{col}+1"], lambda s: s+1)')
					])
		df = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		df = aop(col='a')(df)
		self.assertTrue(series_equal(df['a+1'], df['a']+1))


	def test_args_addition(self):
		aop1 = FromOpScript([
					(1, 1, 'lambda df: apply_and_store(df, ["{col}"], ["{col}+1"], lambda s: s+1)')
					])
		aop2 = FromOpScript([
					(1, 1, 'lambda df: apply_and_store(df, ["{col}"], ["{col}*2"], lambda s: s*2)')
					])
		df = pd.DataFrame (np.random.randn(10,2), columns=['a','b'])
		op = (aop1 + aop2)
		out = (aop1 + aop2)(col='a')(df)
		self.assertTrue(series_equal(df['a+1'], df['a']+1))
		self.assertTrue(series_equal(df['a*2'], df['a']*2))		


	def test_partial_args_1(self):
		aop = FromOpScript([
			(1,1, '''lambda df: df["{col}"].{func}()''')
		])
		aop_sum = aop(func='sum')
		self.assertEqual(type(aop_sum), type(aop))


	def test_partial_args_2(self):
		aop = FromOpScript([
			(1,1, '''lambda df: df["{col}"]*{scalar}''')
		])
		aop_sum = aop(scalar=2)
		df = pd.DataFrame(np.random.randn(10,2), columns=['a','b'])
		out = aop_sum(col='a')(df)
		self.assertTrue(series_equal(df['a']*2, out))


