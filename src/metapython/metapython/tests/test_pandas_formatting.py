import unittest
import nose

from metaprogramming.op.Op import *
from metaprogramming.op.std import *
from metaprogramming.op.pandas_formatting import *


################################################################################
####################[ pandas_formatting ]#######################################
################################################################################

def series_equal(s1, s2, precision=2):
	"""
		given two series composed of floating point numbers,
		asserts that they are equal to 'precision' floating 
		point numbers
	"""
	return all(s1.round(precision) == s2.round(precision))


class Test_pandas_formatting(unittest.TestCase):

	def setUp(self):
		pass

	def test_drop_columns(self):
		df = pd.DataFrame([{'a':1, 'b':2, 'c':3}]*10)
		df = drop_columns(cols=['a', 'b'])(df)
		self.assertNotIn('a', df.columns)
		self.assertNotIn('b', df.columns)

	def test_rename_columns(self):
		df = pd.DataFrame([{'a':1, 'b':2, 'c':3}]*10)
		df = rename_columns(columns={'a':'x'})(df)
		self.assertNotIn('a', df.columns)
		self.assertIn('x', df.columns)

	def test_split_columns(self):
		df = pd.DataFrame(np.random.randn(10,4), columns=['a','b','c','d'])
		left, right = split_columns(left_cols=['a','b'], right_cols=['c','d'])(df)
		self.assertTrue(series_equal(left['a'], df['a']))
		self.assertTrue(series_equal(left['b'], df['b']))		
		self.assertTrue(series_equal(right['c'], df['c']))		
		self.assertTrue(series_equal(right['d'], df['d']))						

	def test_extract_list_element(self):
		df = pd.DataFrame([{'a':[1, 2], 'b':[3, 4]}]*10)
		df = extract_list_element(cols=['a'], index=0)(df)
		self.assertEquals((df['a'] == 1).sum(), len(df))

	def test_extract_dict_value(self):
		df = pd.DataFrame([{'a':{'x':1, 'y':2}, 'b':3}]*10)
		df = extract_dict_value(cols=['a'], key='"x"')(df)
		self.assertIn('a', df.columns)
		self.assertEquals((df['a']==1).sum(), len(df))

	def test_extract_list_dict_values(self):
		df = pd.DataFrame([{'a':[{'x':1, 'y':2}, {'x':3, 'y':4}], 'b':3}]*10)
		df = extract_list_dict_values(cols=['a'], key='"x"')(df)
		self.assertIn('a', df.columns)	
		self.assertEquals(df['a'].str.get(0).sum(), len(df))
		self.assertEquals(df['a'].str.get(1).sum(), len(df)*3)



