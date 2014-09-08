#!/usr/bin/python -W ignore::DeprecationWarning
import pandas as pd
import gensim

from metapython.op.Op import *
from metapython.op.std import *
from metapython.op.pandas_util import *


################################################################################
####################[ GENSIM DICTIONARY/BOW ]###################################
################################################################################

@op(num_out=1)
def dictionary_fit(df, col=None):
	"""
		usage: 
		------
			dictionary = dictionary_fit(col='"a"')(df)
		params: 
		-------
			- col: name of column, in escaped quotes, to fit.
		description: 
		------------
			creates and returns a gensim dictionary for the passed text column,
			which should be tokenized text
	"""
	return gensim.corpora.Dictionary(df[col])


@op(num_out=1)
def dictionary_update(df, dictionary, col=None):
	'''
		usage: 
		------
			dictionary = dictionary_update(col='a')(df, dictionary)
		params: 
		-------
			- col: column containing tokenized text
		description: 
		------------
			updates and returns the passed dictionary with the text from 
			df[col]
	'''	
	dictionary.add_documents(df[col])
	return dictionary


@op(num_out=1)
def dictionary_transform(df, dictionary, col=None):
	"""
		usage:
		------
			df = dictionary_transform(col='a')(df, dictionary)
		params: 
		-------
			- col: name of column containing tokenized text
		description: 
		------------
			converts the specified columns, incols, into gensim bow representations 
			and stores the output in outcols.
	"""
	return apply_and_store(df, [col], [col + '_bow'], lambda s: s.apply(dictionary.doc2bow))


'''
	Op: dictionary_fit_transform
	-------------------------------
	usage:
		df, dictionary = dictionary_fit_transform(col='a')(df)
	params:
		- col: column containing tokenized text
	description:
		fits a dictoinary to the dataframe and returns df with bow column 
		as well as the dictionary
'''
dictionary_fit_transform = 	split_op +\
							(identity_op | dictionary_fit) +\
							(identity_op | split_op) +\
							(dictionary_transform | identity_op)









################################################################################
####################[ GENSIM LDA ]##############################################
################################################################################

@op(num_out=1)
def lda_fit(df, dictionary, col=None, num_topics=100):
	"""
		usage: 
		------
			lda_model = lda_fit(col='a', num_topics=10)(df, dictionary)
		params:
		-------
			- col: column of original tokenized text
			- num_topics: number of lda topics to fit
		description: 
		------------
			Assumes that you have already applied a dictionary transform;
			trains and returns a gensim lda model
	"""
	return gensim.models.ldamodel.LdaModel(df[col + "_bow"], num_topics=num_topics, id2word=dictionary)


@op(num_out=1)
def lda_update(df, lda_model, col=None):
	"""
		usage:
		------
			lda_model = lda_update(col='a')(df, lda_model)
		params:
		-------
			- col: column containing tokenized text. 
		description: 
		------------
			Assumes that you have already applied a dictionary transform;
			updates and returns the supplied gensim lda model with the supplied 
			dataframe 
	"""
	return lda_model.update(df[col +'_bow'])


@op(num_out=1)
def lda_transform(df, lda_model, col=None):
	"""
		usage:
		------
			df = lda_transform(col='a')(df, lda_model)
		params:
		-------
			- col: column containing tokenized text. 
		description:
		------------
			Assumes that you have already applied a dictionary transform;
			given a dataframe and an lda model, puts into {col}_lda a transformed
			version of the text column
	"""
	df = apply_and_store(df, [col + "_bow"], [col + "_lda"], lambda s: s.apply(lambda bow: (lda_model.inference([bow])[0][0])))
	df = apply_and_store(df, [col + "_lda"], [col + "_lda"], lambda s: s.apply(lambda gamma: gamma/gamma.sum()))
	return df


'''
	Op: lda_fit_transform
	------------------------
	usage:
		df, lda_model = lda_fit_transform(col=['a'], num_topics=10)(df)
	params:
		- col: column containing tokenized text to train LDA on
		- num_topics: number of topics to fit LDA to
	description:
		takes in a dataframe, trains lda and returns (transformed_df, lda)
'''
lda_fit_transform = 	dictionary_fit_transform +\
						(split_op | identity_op) +\
						(identity_op | lda_fit) +\
						(identity_op | split_op) +\
						(lda_transform | identity_op)
