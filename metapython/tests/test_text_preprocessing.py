import unittest
import nose

from metaprogramming.op.Op import *
from metaprogramming.op.text_preprocessing import *

################################################################################
####################[ text_preprocessing ]######################################
################################################################################

def series_equal(s1, s2, precision=2):
	"""
		given two series composed of floating point numbers,
		asserts that they are equal to 'precision' floating 
		point numbers
	"""
	return all(s1.round(precision) == s2.round(precision))


class Test_text_preprocessing(unittest.TestCase):

	def setUp(self):
		pass

	def test_vec_str_funcs(self):
		df = pd.DataFrame([{'doc':['THIS', '###is###', 'a', 'TEST']}]*10)
		df = preprocess_raw_text_list(cols=['doc'])(df)
		self.assertIn('doc', df.columns)
		self.assertEquals((df['doc'].str.get(0) == 'this').sum(), len(df))
		self.assertEquals((df['doc'].str.get(1) == 'is').sum(), len(df))
		self.assertEquals((df['doc'].str.get(2) == 'a').sum(), len(df))
		self.assertEquals((df['doc'].str.get(3) == 'test').sum(), len(df))						


	def test_str_join(self):
		df = pd.DataFrame([{'a':['this', 'is'], 'b':['a', 'test']}]*10)
		df = join_text_columns(incols=['a','b'], outcol=['doc'])(df)
		self.assertIn('doc', df.columns)
		self.assertEquals((df['doc'].str.get(0) == 'this').sum(), len(df))
		self.assertEquals((df['doc'].str.get(1) == 'is').sum(), len(df))
		self.assertEquals((df['doc'].str.get(2) == 'a').sum(), len(df))
		self.assertEquals((df['doc'].str.get(3) == 'test').sum(), len(df))	


	def test_remove_stopwords(self):
		df = pd.DataFrame ([{'doc':['this', 'is', 'a', 'test']}]*10)
		df = remove_stopwords(cols=['doc'], langs=['english'])(df)
		self.assertIn('doc', df.columns)
		self.assertEquals((df['doc'].str.get(0) == 'test').sum(), len(df))


	def test_porter_stemmer(self):
		df = pd.DataFrame ([{'doc':['caresses', 'flies', 'dies', 'mules', 'denied']}])
		df = porter_stemmer(cols=['doc'])(df)
		self.assertEquals((df['doc'].str.get(0) == 'caress').sum(), len(df))
		self.assertEquals((df['doc'].str.get(1) == 'fli').sum(), len(df))
		self.assertEquals((df['doc'].str.get(2) == 'die').sum(), len(df))
		self.assertEquals((df['doc'].str.get(3) == 'mule').sum(), len(df))	
		self.assertEquals((df['doc'].str.get(4) == 'deni').sum(), len(df))	

