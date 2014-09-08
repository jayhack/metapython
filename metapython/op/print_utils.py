def dump_ops_to_file(ops, filepath):
	'''
	dumps all ops in ops to the file as functions.

	parameters:
	-	ops: a list of (op, name) TUPLES. name is the string to call that specific op's function (i.e, linkedin_preprocess)

	returns:
	none

	notes:
	if the same name is used twice, will throw an error.
	'''
	#1 open the write file
	writefile = open(filepath, 'w')
	#2 store a set of seen names
	seen_names = set()
	#3 iterate through ops and dump functions
	for op, name in ops:
		if name in seen_names:
			raise Exception ("You're trying to re-use a function name. Don't do that.")
		else:
			seen_names.add(name)
		writefile.write(op.to_function_script(function_name=name) + '\n\n')
		seen_names.add(name)
	#4 close the file
	writefile.close()