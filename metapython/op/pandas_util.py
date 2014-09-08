import inspect
import pandas as pd

def present_cols (df, cols):
	""""
		returns: intersection of cols and df.columns
	"""
	return list(set(df.columns).intersection(set(cols)))


def absent_cols (df, cols):
	"""
		returns: set difference of df.columns and columns
	"""
	return list(set(df.columns).difference (set(cols)))


def combine_list_cols(columns):
	assert len(columns) >= 1
	combo = columns[0]
	for c in columns[1:]:
		combo += c
	return combo


def apply_and_store(obj, access_keys, store_keys, operation):
	"""
		usage:
			apply_and_store(df, ['a','b'], ['a+1','b+1'], lambda s:s+1)
		params:
			- obj: object (pandas df...) to operate on 
			- access_keys: name of columns to apply operation to
			- store_keys: name of columns to store output in
			- operation: operation to apply
		description:
			applies the operation to df[ak] and stores it in df[sk],
			for each (ak,sk) in zip(access_keys, store_keys). returns 
			the modified obj.
	"""
	#=====[ Step 1: get number of args to operation	]=====
	num_args = len(inspect.getargspec(operation).args)

	#=====[ Step 1: type checks	]=====
	if type(access_keys) != list or type(store_keys) != list:
		raise TypeError("apply_and_store: access/store_keys must be a list! you had %s and %s" % (type(access_keys), type(store_keys)))

	#=====[ Step 2: handle one-to-one mappings 	]=====
	if (len(access_keys) == len(store_keys)) and num_args == 1:
		for ak, sk in zip(access_keys, store_keys):
			obj[sk] = operation(obj[ak])

	#=====[ Step 3: handle many-to-one mappings	]=====
	elif (len(store_keys) == 1) and (num_args == 1) and (len(access_keys) > 1):
		obj[store_keys[0]] = operation(obj[access_keys])

	#=====[ Step 4: other cases that fail	]=====
	else:
		assert False

	return obj


def add_tag (l, tag):
	"""
		adds 'tag' to each element in l 
	"""
	return [w + '_' + tag for w in l] if type(l) == list else []





