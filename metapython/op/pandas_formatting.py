"""
 	Module: pandas_formatting
	=========================
	extends the standard library to include Ops for formatting 
	pandas dataframes.

	Summer 2015
"""
import numpy as np
import pandas as pd

from metapython.op.Op import *
from metapython.op.std import *
from metapython.op.pandas_util import *


################################################################################
####################[ COLUMN ORGANIZATION ]#####################################
################################################################################

@op(num_out=1)
def drop_columns(df, cols=None):
	"""
		usage: 
		------
			drop_columns(df, cols=['a','b'])
		params: 
		-------
			- cols: list of names of columns to drop.
		description:
		------------
			drops the named columns from the dataframe; only 
			attempts to drop those that are actually present.
	"""
	return df.drop(present_cols(df, cols), axis=1)


@op(num_out=1)
def keep_columns(df, cols=None):
	"""
		usage: 
		------
			keep_columns(cols=['a','b'])(df)
		params:
		-------
			- cols: list of strings naming columns to keep
		description:
		------------
			drops all columns from the supplied dataframe that are 
			not in the supplied list.
	"""
	return df.drop(absent_cols(df, cols), axis=1)


@op(num_out=1)
def rename_columns(df, columns=None):
	"""
		usage:
		------
			rename_columns(cols=['a','b'])(df)
		params:
		-------
			- cols: list of strings naming columns to drop
		description:
		------------
			drops the columns named by 'cols' from supplied pandas
			dataframe, returns resulting dataframe
	"""
	return df.rename(columns=columns)


@op(num_out=1)
def select_columns(df, cols=None):
	"""
		usage:
		------
			df = select_columns(cols=['a','b'])(df)
		params:
		-------
			- cols: name of columns you want to select 
		description: 
		------------
			returns a view into the given dataframe, only showing 
			the columns you have specified
	"""
	return df[cols]


@op(num_out=1)
def split_columns(df, right_cols=None, left_cols=None):
	"""
		usage:
		------ 
			df1, df2 = split_columns(left_cols=['a','b'], right_cols=['c','d'])(df)
		params:
		-------
			- left_cols: column names for the left half
			- right_cols: column names for the right half
		description:
		------------
			given a dataframe, will split it into two pieces based on column names
			and return the results
	"""
	return df[left_cols], df[right_cols]










################################################################################
####################[ DATA CLEANING ]###########################################
################################################################################

@op(num_out=1)
def extract_list_element(df, cols=None, index=0):
	"""
		usage: 
			extract_list_element(df, cols=['a'], index=0)
		params: 
			- cols: names of columns with each entry consisting of a list
			- index: index into list that you want to extract
		description: 
			converts each named column to a series containing only the
			{index}th elements of its original elements.
	"""
	for col in cols:
		df[col] = df[col].str.get(index)
	return df



@op(num_out=1)
def extract_dict_value(df, cols=None, key=None):
	"""''
		usage: 
		------
			extract_dict_value(col='a', key='b')(df)
		params:
		-------
			- col: column containing a dict for each entry
			- key: key of dict values to extract
		description: 
		------------
			outputs into column named {col}[{key}] the result of extracting the value 
			described by 'key' in the corresponding entry in 'incol'
	"""
	for col in cols:
		df[col] = df[col].apply(lambda d: d[key] if type(d) == dict and key in d else np.nan)
	return df


@op(num_out=1)
def extract_list_dict_values(df, cols=None, key=None):
	"""
		usage: 
		------
			extract_list_dict_values(col='a', key='b', outcol='c')(df)
		params:
		-------
			- col: column containing a list of dicts for each entry
			- key: key of dict value to extract
		description:
		------------
			outputs into column named {incol}_{key} the result of extracting the values 
			described by 'key' in each element of the corresponding entry in 'incol'
	"""
	for col in cols:
		df[col] = df[col].apply(lambda l: [d[key] for d in l] if type(l) == list else np.nan)
	return df



'''
	Op: discretize_labels
	------------------------
	usage:
		df_discrete = discretize_labels(df[['country','gender']])
	description:
		given a dataframe where each column contains labels, e.g. in a "gender" column,
		this will return a dataframe where there is a one-hot numerical representation 
		of it instead.
'''
discretize_labels = FromOpScript([
	(1, 1, '''lambda df: pd.concat([pd.get_dummies(df[col]) for col in df.columns], axis=1)''')
])







