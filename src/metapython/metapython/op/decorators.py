import inspect
import re
from functools import wraps, partial

from metaprogramming.op.Op import *

def op(num_out=1, func=None):
	'''
		decorator/function: op
		----------------------
		decorator for creating Ops out of functions

		Ideal operation:
			1-
			@op(num_out=1)
			def sum_column(df):
				return df['a'].sum()
			2-
			split_op = op(lambda x: x.split())
	'''
	if func is None:
		# CASE 1: must have been called as @op(1) or @op(num_out=1)
		# we'll return a partial of opcall with num_out set to what's given
		# then the @op(1) becomes "@partial(opcall)", and when it's called it'll be f = (partial(opcall(f))) as desired
		return partial(opcall, num_out)

	else:
		# CASE 2: must have been called as op(1, func) where func is probably, but not definitely, a lambda
		return opcall(num_out, func)


def opcall(num_out, func):
	func_name, argspec, operations = parse_func_source(func)
	return Op_from_function_params(num_out, func_name, argspec, operations)


def parse_lambda(lambda_lines):
	pattern = 'op\((.*)\)'
	lambda_string = lambda_lines[0]
	matches = re.findall(pattern, lambda_string)
	
	if len(matches) > 1:
		raise Exception("Too many op(...) instantiations in one line, can't figure out which is which.")
	lambda_func = ','.join(matches[0].split(',')[1:]) # 0 assumes that it's called as op(num_out, lambda) as matches[0] will be num_out,lambda

	func_name = '_lambda_' + lambda_string.split('=')[0].rstrip().lstrip() # assumes that it's called as something = op(...). 
	operations = lambda_func
	return func_name, operations
	

def parse_func_source(func):
	"""
		gets the variables and source code of a function
		returns:
			func_name, num_args, num_outputs, args, operations
	"""
	lines 		= filter(lambda v: v != u'', inspect.getsourcelines(func)[0])
	if len(lines)==1:
		# CASE: MUST BE FROM A LAMBDA FUNCTION
		func_name, operations = parse_lambda(lines)
		argspec = inspect.getargspec(func)
		return func_name, argspec, operations

	else:
		if 'return' not in lines[-1]:
			raise Exception("Not well formed op script. No return line (got %s)" % return_line)
		func_name 	= func.func_name
		argspec 	= inspect.getargspec(func)
		operations 	= ''.join(lines[2:])
		return func_name, argspec, operations


def create_symbol_table(num_out, func_name, argspec, operations):
	# step 1: get num args, outputs
	function_num_args = len(argspec.args)
	function_num_outputs = num_out
	# check if defaults is None
	if argspec.defaults is None:
		num_defaults = 0
		keyword_args_replaced = []
	else:
		num_defaults = len(argspec.defaults)
		keyword_args = argspec.args[-num_defaults:]
		keyword_args_replaced = ['%s={%s}' % (kwarg,kwarg) for kwarg in keyword_args]
	
	# nonkeyword args stay the same
	nonkeyword_args = argspec.args[:function_num_args - num_defaults]
	# join the args
	function_args = ','.join(nonkeyword_args + keyword_args_replaced)
	# return the symbol table and the number of non-keyword args, for ops_df
	return pd.DataFrame([{'func_name':func_name, 'num_args':function_num_args, 'num_outputs':function_num_outputs, 'args':function_args, 'operations':operations}]), len(nonkeyword_args)


def create_ops_df(num_out, func_name, num_in):
	ops_df = pd.DataFrame([{'operation':func_name, 'num_in':num_in, 'num_out': num_out, 'nop':False}])
	return ops_df


def Op_from_function_params(num_out, func_name, argspec, operations):
	"""
	    a special Op that allows passing multi-line defined functions rather than just one line lambdas.
		usage: test_mop = Mop(1, 1, '''x
						return x''')
			
	potentially doesn't even need to have the 1, 1. also, functionality could be added to Op.
		"""	
	symbol_table, num_in = create_symbol_table(num_out, func_name,argspec, operations)
	ops_df = create_ops_df(num_out, func_name, num_in)
	return Op(ops_df, symbol_table)

		


