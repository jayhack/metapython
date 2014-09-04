"""
	Module: std
	===========
	contains the standard ops that apply to all data types
"""
from metaprogramming.op.Op import *
from metaprogramming.op.decorators import *

################################################################################
####################[ Basic Operand Manipulation ]##############################
################################################################################

@op(num_out=1)
def identity_op(x):
	"""
		usage: 
		------
			o_0 = identity_op(o_0)
		description:
		------------
			returns its input as an output
	"""
	return x


@op(num_out=2)
def split_op(x):
	"""
		usage:
		------
			(o_0_1, o_0_2) = split_op(o_0)
		description:
		------------
			returns its input twice 
	"""
	return x, x


@op(num_out=2)
def swap_op(x, y):
	"""
		usage:
		------
			o_0, o_1 = swap_op(o_0, o_1)
		description:
		------------
			swaps the contents of o_0, and o_1
	"""
	return y, x





################################################################################
####################[ Working on DFS ]##########################################
################################################################################

'''
	ArgOp: apply_inplace
	--------------------
	usage:
		add_one = apply_inplace(func_str=lambda x:x+1)
		df = add_one(cols=['a','b'])(df)
	params:
		- cols: names of columns to apply operation to
		- func_str: string of lambda function to be applied
	description:
		base ArgOp for all Ops that apply an operation to columns and 
		store the results back in the same columns; one to one
'''
apply_inplace = FromOpScript([
	(1,1, '''lambda df: apply_and_store(df, {cols}, {cols}, {func_str})''')
])


'''
	ArgOp: apply_store_external
	---------------------------
	usage:
		add_one = apply_store_external(func_str=lambda x:x+1)
		df = add_one(incols=['a','b'], outcols=['c','d'])
	params:
		- incols: names of columns to apply operation to 
		- outcols: names of columns to store output in
		- func_str: string of lambda functio nto be applied
	description:
		base ArgOp for all Ops that apply an operation to columns and 
		store the results in a new set of columns; one to one
'''
apply_store_external = FromOpScript([
	(1,1, '''lambda df: apply_and_store(df, {incols}, {outcols}, {func_str})''')
])


'''
	ArgOp: store_transformation
	---------------------------
	usage:
		sum_cols = store_transformation(func_str=lambda x,y:x+1)
		df = sum_cols(cols=['a','b'], outcol=['a+b'])(df)
	params:
		- incols: columns that function takes in
		- outcol: column to store output in, in a list.
		- func_str: string of function to be applied
	description:
		applies the transformation described by func_str to df[cols] 
		and stores the result in outcol
'''
store_transformation = FromOpScript([
	(1,1, '''lambda df: apply_and_store(df, {incols}, {outcol}, {func_str})''')
])