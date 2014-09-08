'''
 	Module: pandas_manipulation
	===========================
	extends the standard library to include Ops for manipulating
	pandas dataframes, including split-apply-combine paradigm.

	Jay Hack
	jay@205consulting.com
	Summer 2015
'''
import numpy as np
import pandas as pd

from metapython.op.Op import *
from metapython.op.pandas_util import *
from metapython.op.std import *

'''
	Op: groupby/agg
	------------------
	usage:
		session_lens = (groupby(col='s_id') + agg(func_str='count'))(df)
	params:
		- col: column to group by
		- func_str: string of function to aggregate by
	description:
		groupby operations
'''
groupby = FromOpScript([
	(1, 1, '''lambda df: df.groupby("{col}")''')
])
aggby = FromOpScript([
	(1, 1, '''lambda grouped: grouped.agg({func_str})''')
])


'''
	Op: grouped_to_dfs
	---------------------
	usage:
		dfs = grouped_to_dfs(df.groupby('s_id'), df)
	description:
		converts a pandas GroupBy object into a dict mapping 
		groupby key to a dataframe of entries it exists in.
'''
grouped_to_dfs = FromOpScript([
	(2, 1, '''lambda grouped, df: {key: df.ix[indices] for key, indices in grouped.groups.iteritems()}''')
])


'''
	Op: split_by_key
	-------------------
	usage: 
		dfs = split_by_key(key_col='s_id')(df)
	params:
		- col: name of column to split on
	description:
		given a df and the name of a column containing keys, this returns 
		a dict mapping the different keys to dataframes of entries containing 
		them
'''
split_by_key = 	split_op +\
				(groupby(col='{key_col}') | identity_op) +\
				grouped_to_dfs




