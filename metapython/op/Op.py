import re
import sys
import time
import hashlib
from copy import copy
from lazy_format import LazyFormat
from datetime import timedelta

import numpy as np
import scipy as sp
import pandas as pd
import gensim
import random
import sklearn
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import nltk
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt

from metapython.op.pandas_util import *


################################################################################
####################[ BaseOp: Functional Queries ]##############################
################################################################################

class BaseOp(object):
	"""
		Ideal Operation:
			Op (operations) (dataframes)
			o1 = Op (operations)
			o2 = Op (other operations)
			o3 = o1 + o2
			o4 = o2 - o1
			o5 = o1 * 5
			o1[1:-1] (dataframes)
			o2["process_text":"run_inference"] (dataframes)
			o2["step a":"step b"] + o2["step c":"step d"] (dataframes)
			for command in o2:
				...
	"""

	def __init__ (self, ops_df, symbol_table, verbose=False):

		#=====[ print options	]=====
		self.verbose = verbose
		self.set_ops_df(ops_df)
		self.set_symbol_table(symbol_table)

		self.num_in, self.num_out = self.get_cardinality(self.ops_df)
		self.compiled_df = None

		
	def set_ops_df(self, ops_df):
		"""
			sets self.ops_df after type-checking.
		"""
		assert type(ops_df) == pd.DataFrame
		self.ops_df = ops_df


	def set_symbol_table(self, symbol_table):
		"""
			sets the internal symbol table to the passed-in df 
			after type-checking. also checks that no function names 
			are repeated.
			called by join_ops and add_ops
		"""
		assert type(symbol_table) == pd.DataFrame
	
		#=====[ Remove duplicates and null elements	]=====
		symbol_table = symbol_table.ix[symbol_table.func_name.notnull()]
		symbol_table = symbol_table.drop_duplicates()
		if symbol_table.func_name.nunique() != len(symbol_table.func_name):
			print "WARNING! The symbol table for this op contains duplicate function names. If these aren't the same function, you'll run into problems."

		self.symbol_table = symbol_table
		self.symbol_table.index = self.symbol_table.func_name



	def get_cardinality(self, ops_df):
		"""
			given an ops_df, this will determine its in/out cardinality and mark it 
			as such. (lines on top/bottom indicating cardinality)
			NOTE: this doesn't apply during joins, which are dealt with specially 
			in the join function
		"""
		no_nops_df = ops_df.ix[~ops_df['nop']]
		if len(no_nops_df) > 0:
			# assert list(no_nops_df.num_out)[:-1] == list(no_nops_df.num_in)[1:] #not true on joins...
			num_in, num_out = no_nops_df.iloc[0].num_in, no_nops_df.iloc[-1].num_out
		else:
			num_in, num_out = 0, 0
		return num_in, num_out


	def get_input_assignment_string(self, operands):
		"""
			Assembles string for assigning inputs to the o_stack
		"""
		if not len(operands) == self.num_in:
			raise Exception("The amount of arguments passed in was not equal to self.num_in (passed in %s, num_in was %s)" % (len(operands), self.num_in))
		if len(operands) > 0:
			return 'o_stack = list(operands)'
		else:
			return 'o_stack = []'


	def get_rhs_string(self, op_row):
		"""
			Assembles string for application of operation.
			resembles:
				'((lambda x: x**2)(2)),)'
				or
				'import json'
		"""
		if op_row.num_in > 0 and not op_row.nop:
			if op_row.num_out > 1:
				return '(%s)(*o_stack[:%s])' % (op_row.operation, op_row.num_in)
			else:
				return '((%s)(*o_stack[:%s]),)' % (op_row.operation, op_row.num_in)
		elif op_row.num_in == 0 and not op_row.nop:
			if op_row.num_out > 1:
				return '(%s)()' % op_row.operation
			else:
				return '((%s)(),)' % op_row.operation
		else:
			return op_row.operation


	def get_lhs_string(self, op_row):
		"""
			Assembles string for assignment of output of 
			operation.
			resembles:
				'o_stack[:3] = ''
				or 
				''
		"""
		if op_row.num_out > 0:
			return 'o_stack[:%s] = ' % op_row.num_out
		else:
			return ''


	def get_return_string(self, num_out):
		"""
			Assembles a string that can be evaluated in order to return 
			from the function 
		"""
		if self.num_out > 0:
			if self.num_out > 1:
				return 'tuple(o_stack[:%s])' % self.num_out
			elif self.num_out == 1:
				return 'o_stack[0]' % num_out
		else:
			return 'None'


	def compile(self):
		"""
			compile:
			--------

			iterates through the symbol table and then the ops_df and 
			compiles the script into a new dataframe, compiled_df, in 
			which each row has one value ("script_string") and the df 
			can be executed line by line.
		"""
		#=====[ Initialize a list of strings to be turned into a dataframe ]=====
		script_strings = []


		#=====[ Iterate through rows of the symbol table ]=====
		for ix, row in self.symbol_table.iterrows():

			#===[ Initialize exec string ]===#
			exec_str = ''

			if row.func_name.startswith('_lambda_'):
				# CASE: it's a lambda function, just exec func_name = lambda...
				exec_str += '%s = %s' % (row.func_name, row.operations)

			else:
				#===[ Get function definition ]===#
				function_definition = 'def %s(%s):\n' % (row.func_name, row.args)
				exec_str += function_definition

				#===[ Add operation lines ] ===#
				exec_str += row.operations

			#===[ Execute code ] ===#			
			script_strings.append({'script_string':exec_str, 'return_str':False})


		#=====[ Iterate through actual operations	]=====
		for ix, row in self.ops_df.iterrows ():

			#=====[ Get step code ]=====
			rhs_str 	= self.get_rhs_string(row)
			lhs_str 	= self.get_lhs_string(row)
			exec_str 	= lhs_str + rhs_str

			#=====[ Execute step code	]=====
			script_strings.append({'script_string':exec_str, 'return_str':False})

		#=====[ Return values	]=====
		return_str = self.get_return_string(self.num_out)
		
		script_strings.append({'script_string':return_str, 'return_str':True})

		compiled_df = pd.DataFrame(script_strings)
		return compiled_df


	def __call__ (self, *operands):
		"""
			MAGIC: __call__
			---------------
			applies the operations contained in this Op to the specified 
			dataframe
		"""
		if self.verbose:
			print ">>>>>>>>>>[ Op Begin ]<<<<<<<<<<"

		#=====[ Compile if necessary	]=====
		if self.compiled_df is None:
			self.compiled_df = self.compile()

		#=====[ Reassign operands to strings o_0...o_n	]=====
		assignment_str = self.get_input_assignment_string(operands)
		if self.verbose:
			print '~ %s' % assignment_str
		exec assignment_str
	
		#=====[ Iterate through rows of the compiled df and exec the strings ]=====
		for ix, row in self.compiled_df.iterrows():
			if row.return_str:
				if self.verbose:
					print '~ %s' % row.script_string
					print ">>>>>>>>>>[ Op End ]<<<<<<<<<<"
				return eval(row.script_string)
			else:
				if self.verbose:
					print '~ %s' % row.script_string
				exec row.script_string


	def __add__ (self, other):
		"""
			returns concatenation of the two operations
			op3 = op1 + op2
		"""
		return add_ops(self, other)


	def __or__ (self, other):
		"""
			JOIN operation 
			--------------
			op3 = (op1 | op2)
			op3 intput/output:
				input: (op1_in1,...,op1_inn, op2_in1,...,op2_inn)
				output: (op1_out1,...,op1_outn, op2_out1,...,op2_outn)
		"""
		return join_ops(self, other)


	def __getitem__ (self, indexer):
		"""
			returns either a single operation or a slice 
		"""
		if type(indexer) == str:
			return Op(pd.DataFrame([self.ops_df.iloc[indexer]]))
		elif type(indexer) == slice:
			return Op(self.ops_df.iloc[indexer.start:indexer.stop])






################################################################################
####################[ Op ]######################################################
################################################################################

class Op(BaseOp):
	'''
		a level of abstraction above BaseOp. 

		- Deals with putting in arguments
		- Assumes an input of ops_df and symbol_table
			(these are parsed in the constructor functions, i.e.
				from_lambda and from_function)
	'''
	def __init__(self, ops_df, symbol_table):
		super(Op, self).__init__(ops_df, symbol_table)


	def ops_df_is_formatted(self, ops_df):
		"""
			returns true if there are still args to fill in
		"""
		variables = re.findall('{[A-Za-z_]+}', self.get_op_str (ops_df))
		return len(variables) == 0


	def symbol_table_is_formatted(self, symbol_table):
		"""
			returns true if there are still args to fill in
		"""
		variables = re.findall('{[A-Za-z_]+}', self.get_func_str (symbol_table))
		return len(variables) == 0


	def is_completely_formatted(self, ops_df, symbol_table):
		
		return (self.ops_df_is_formatted(ops_df) and self.symbol_table_is_formatted(symbol_table))


	def get_op_str (self, ops_df):
		"""
			returns a single string containing all operations
			contained in script
		"""
		if type(ops_df) == pd.core.frame.DataFrame:
			return '||'.join(ops_df['operation'])
		else:
			raise TypeError


	def insert_op_str (self, op_str, ops_df):
		"""
			returns script with op_str inserted into it
		"""
		ops_df['operation'] = op_str.split('||')
		return ops_df


	def get_func_str (self, symbol_table):
		"""
			returns a single string containing all operations
			contained in script
		"""
		if type(symbol_table) == pd.core.frame.DataFrame:
			return '||'.join(symbol_table['args'])
		else:
			raise TypeError


	def insert_func_str (self, func_str, symbol_table):
		"""
			returns script with op_str inserted into it
		"""
		symbol_table['args'] = func_str.split('||')
		return symbol_table


	def __call__ (self, *args, **kwargs):
		"""
			inserts provided arguments into the ops df;
			returns Op if all arguments are filled, otherwise returns
			another Op.
		"""
		#=====[ Step 1: insert args into ops_df and symbol table	]=====
		op_str = LazyFormat(self.get_op_str(self.ops_df)).format(**kwargs)
		new_ops_df = self.ops_df.copy()
		self.insert_op_str(op_str, new_ops_df)

		func_str = LazyFormat(self.get_func_str(self.symbol_table)).format(**kwargs)
		new_symbol_table = self.symbol_table.copy()
		self.insert_func_str(func_str, new_symbol_table)

		#=====[ Case: formatted	and enough args passed in ]=====
		if self.is_completely_formatted(new_ops_df, new_symbol_table) and len(args) == self.num_in:
			base_op = BaseOp(new_ops_df, new_symbol_table)
			base_op.num_in = self.num_in
			base_op.num_out = self.num_out
			return base_op(*args)
			

		#=====[ Case: unformatted, or args weren't passed in (return a new op) 	]=====
		else:
			new_op = copy(self)
			new_op.ops_df = new_ops_df
			new_op.set_symbol_table(new_symbol_table)
			return new_op






################################################################################
####################[ CREATION ]################################################
################################################################################



def FromOpScript(op_script):
	"""
		converts an op_script into an Op

		op_script syntax:
			[
				(# args in, # args out, str(operation to apply)),
				...
			]
	"""
	#=====[ Step 1: ops_df	]=====
	assert type(op_script) == list
	ops_df = pd.DataFrame (op_script, columns=['num_in', 'num_out', 'operation'])
	ops_df['operation'].str.strip()
	ops_df['nop'] = ((ops_df['num_in'] == 0) & (ops_df['num_out'] == 0))

	#=====[ Step 2: create empty symbol table	]=====
	symbol_table = pd.DataFrame(columns=['func_name','num_args','num_outputs','args','operations'])
	return Op(ops_df, symbol_table)




################################################################################
####################[ FromOpScript ]############################################
################################################################################

def FromOpScript(op_script):
	"""
		converts an op_script into an Op

		op_script syntax:
			[
				(# args in, # args out, str(operation to apply)),
				...
			]
	"""
	#=====[ Step 1: ops_df	]=====
	assert type(op_script) == list
	ops_df = pd.DataFrame (op_script, columns=['num_in', 'num_out', 'operation'])
	ops_df['operation'].str.strip()
	ops_df['nop'] = ((ops_df['num_in'] == 0) & (ops_df['num_out'] == 0))

	#=====[ Step 2: create empty symbol table	]=====
	symbol_table = pd.DataFrame(columns=['func_name','num_args','num_outputs','args','operations'])
	return Op(ops_df, symbol_table)






################################################################################
####################[ CHAINING/JOINING ]########################################
################################################################################

def add_ops(op1, op2):
	"""
		given two Ops (either or both ArgOps), this returns them 
		chained together 
	"""
	# assert (op1.num_out == op2.num_in) or (op1.num_out == 0) or (op2.num_in == 0) #not true in joins...
	chained_df = pd.concat([op1.ops_df, op2.ops_df])
	chained_symbol_table = pd.concat([op1.symbol_table, op2.symbol_table])
	op = Op(chained_df, chained_symbol_table)
	op.num_in = op1.num_in if op1.num_in > 0 else op2.num_in
	op.num_out = op2.num_out if op2.num_out > 0 else op1.num_out
	return op


'''
	ArgOps: for Joining
	-------------------
	params:
		{_name}: unique name for the new, joined Op, created at time 
					of joining
		{_left_in}: number of inputs to the left one
		{_left_out}: number of outputs from the left one
		{_right_in}: number of inputs to the right one
		{_right_out}: number of outputs from the right one
'''
save_r_inputs = FromOpScript([(0,0, 		'right_ins_save_{_name} = o_stack[{_left_in}:]')])
save_l_outputs = FromOpScript([(0,0, 		'left_outs_save_{_name} = o_stack[:{_left_out}]')])	
place_r_inputs = FromOpScript([(0,0,		'o_stack[:{_right_in}] = right_ins_save_{_name}')])
place_r_outputs = FromOpScript([(0,0, 		'o_stack[{_left_out}:{_left_out}+{_right_out}] = o_stack[:{_right_out}]')])
place_l_outputs = FromOpScript([(0,0,		'o_stack[0:{_left_out}] = left_outs_save_{_name}')])

def join_ops(op1, op2):
	"""
		given two Ops (either or both ArgOps), this returns them 
		joined together 
	"""
	aop = (
				save_r_inputs +\
				op1 + save_l_outputs +\
				place_r_inputs + op2 + place_r_outputs +\
				place_l_outputs
			)(
				_name=hashlib.sha256(str(time.time())).hexdigest(),
				_left_in = op1.num_in, _left_out = op1.num_out,
				_right_in = op2.num_in, _right_out = op2.num_out,
			)
	aop.num_in = op1.num_in + op2.num_in
	aop.num_out = op1.num_out + op2.num_out
	aop.set_symbol_table(pd.concat([op1.symbol_table, op2.symbol_table]))
	return aop

