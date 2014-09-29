import numpy as np
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer

from metapython.op.Op import *
from metapython.op.decorators import *
from metapython.op.std import *
from metapython.op.pandas_util import *

################################################################################
####################[ String Manipulation Functions ]###########################
################################################################################
"""
	Op: string functions 
	--------------------
	usage: 
		[..function name...](cols=['a','b'])(df)
	params:
		- cols: list of names of columns to apply operation to
	description:
		for each of the named columns, this will apply the supplied pandas 
		vectorized string function inplace.
"""
str_fillna 				= apply_inplace(func_str='''lambda s: s.fillna("")''')
vec_str_func 			= apply_inplace(func_str='''lambda s: s.str.{func_str}''')
str_lower 				= vec_str_func(func_str='''lower()''')
str_split 				= vec_str_func(func_str='''split()''')
str_join 				= vec_str_func(func_str='''join(" ")''')
str_remove_nonalpha 	= vec_str_func(func_str='''replace("[^A-Za-z ]", "")''')


'''
	Op: preprocess_raw_text[_list]
	---------------------------------
	usage:
		preprocess_raw_text[_list](cols=['a','b'])(df)
	params:
		- cols: list of columns apply textual preprocessing to
	description:
		for each named column in {cols}, this will do the following
		operationsin place:
			- decode to utf-8
			- translate foreign characters to their english equivalents
			- convert to lowercase
			- remove punctuation
			- split on whitespace
'''
preprocess_raw_text = str_fillna + str_remove_nonalpha + str_lower  + str_split
preprocess_raw_text_list = str_join + preprocess_raw_text







################################################################################
####################[ Stopwords/Stemming ]######################################
################################################################################

@op(num_out=1)
def remove_words_in_set(df, wordset, cols=None):
	'''
		usage:
		------
			df = remove_words_in_set(df, wordset, cols=['a','b'])
		params:
		------
		- cols: list of names of columns containing tokenized text to remove 
				words from
		description:
		------------
			operating on a df and a set of words, removes those words from all named 
			columns of the dataframe
	'''
	return apply_and_store(df, cols, cols, lambda s: s.apply(lambda l: filter(lambda w: w not in wordset, l)))


@op(num_out=1)
def compile_stopwords(langs=['english']):
	"""
		usage:
		------
			stopwords = compile_stopwords(langs=['english', 'german'])
		params:
		-------
			- langs: list of lowercase languages 
		description:
		------------
			returns a set of stopwords for the appropriate languages
	"""
	return set.union(*[set(nltk.corpus.stopwords.words(l)) for l in langs])


"""
	Op: remove_stopwords
	--------------------
	usage:
		remove_stopwords(df, langs=['english', 'danish', 'german'])
	params:
		- cols: list of names of columns containing tokenized text to remove 
				stopwords from
	description:
		operating on a df and a list of languages, this will remove the stopwords from 
		the specified languages
"""
remove_stopwords = 	(identity_op | compile_stopwords) +\
					remove_words_in_set


@op(num_out=1)
def porter_stemmer(df, cols=None):
	"""
	    usage:
	    ------
	        porter_stemmer(cols=['a'])(df)
	    params:
	    -------
			- cols: column containing a tokenized list of words to be stemmed
	    description:
	    ------------
	        applies the nltk porter stemmer to the columns in 'cols'
	"""
	return apply_and_store(df, cols, cols, lambda s: s.apply(lambda l: [PorterStemmer().stem(w) for w in l]))








################################################################################
####################[ Managing Collections of Text Cols]########################
################################################################################

'''
	Op: join_text_columns
	---------------------
	usage: 
		join_text_columns(incols=['a', 'b', 'c'], outcol='abc_joined')(df)
	params: 
		- incols: list of columns containing tokenized text to be 
				joined
		- outcol: name of column to store joined lists
	description: 
		concatenates the tokenized text lists contained in df[incols] and 
		stores it in df[outcol]
'''
join_text_columns = store_transformation(func_str='''lambda df: combine_list_cols([df[c] for c in df.columns])''')


'''
	Op: dedupe_list
	---------------
	usage: 
		dedupe_list (cols=['a']) (df)
	params:
		- cols: list of columns containing lists as values
	description:
		remove duplicates from the list.

'''
@op(num_out=1)
def dedupe_list(df, cols=None):
	for col in cols:
		df[col] = df[col].apply(lambda l: list(set(l)) if type(l) == list else l)
	return df
