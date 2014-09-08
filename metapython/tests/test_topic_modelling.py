import unittest
import nose

from metaprogramming.op.Op import *
from metaprogramming.op.std import *
from metaprogramming.op.topic_modelling import *

################################################################################
####################[ topic_modelling ]#########################################
################################################################################

def series_equal(s1, s2, precision=2):
	"""
		given two series composed of floating point numbers,
		asserts that they are equal to 'precision' floating 
		point numbers
	"""
	return all(s1.round(precision) == s2.round(precision))


class Test_topic_modelling(unittest.TestCase):

	def setUp(self):
		pass

	def test_dictionary_fit(self):
		df = pd.DataFrame([{'a':['this', 'is', 'a', 'test']}]*10)
		dictionary = dictionary_fit(col='"a"')(df)
		for w in ['this', 'is', 'a', 'test']:
			self.assertIn(w, dictionary.values())


	def test_dictionary_transform(self):
		df = pd.DataFrame([{'a':['this', 'is', 'a', 'test']}]*10)
		dictionary = dictionary_fit(col='"a"')(df)
		df = dictionary_transform(col='"a"')(df, dictionary)
		for ix, w in enumerate([(0, 1), (1, 1), (2, 1), (3, 1)]):
			self.assertEquals((df['a_bow'].str.get(ix) == w).sum(), len(df))


	def test_dictionary_fit_transform(self):
		df = pd.DataFrame([{'a':['this', 'is', 'a', 'test']}]*10)
		df, dictionary = dictionary_fit_transform(col='"a"')(df)
		for w in ['this', 'is', 'a', 'test']:
			self.assertIn(w, dictionary.values())
		for ix, w in enumerate([(0, 1), (1, 1), (2, 1), (3, 1)]):
			self.assertEquals((df['a_bow'].str.get(ix) == w).sum(), len(df))


	def test_lda_fit(self):
		df = pd.DataFrame([{'a':['this', 'is', 'a', 'test']}]*10)
		df, dictionary = dictionary_fit_transform(col='"a"')(df)
		lda_model = lda_fit(col='"a"', num_topics=2)(df, dictionary)
		self.assertEquals(len(lda_model.show_topics()), 2)


	def test_lda_transform(self):
		df = pd.DataFrame([{'a':['this', 'is', 'a', 'test']}]*10)
		df, dictionary = dictionary_fit_transform(col='"a"')(df)
		lda_model = lda_fit(col='"a"', num_topics=2)(df, dictionary)
		df = lda_transform(col='"a"')(df, lda_model)
		self.assertEquals(len(df['a_lda'].iloc[0]), 2)


	def test_lda_fit_transform(self):
		df = pd.DataFrame([{'a':['this', 'is', 'a', 'test']}]*10)
		df, dictionary = dictionary_fit_transform(col='"a"')(df)
		df, lda_model = lda_fit_transform(col='"a"', num_topics=2)(df)
		self.assertEquals(len(lda_model.show_topics()), 2)
		self.assertEquals(len(df['a_lda'].iloc[0]), 2)