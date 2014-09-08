import os
import sys
import time
import json
import simplejson
import csv

from metapython.stor.Stor import *
from metapython.stor.MemoryStor import *


def blocks_from_generator(gen, size):
	"""
		given a generator and a blocksize, this will
		generate all blocks of 'size' elements that 
		come out of the generator, as lists
	"""
	counter = 0
	current_block = []
	for x in gen:
		current_block.append(x)
		counter += 1
		if counter % size == 0:
			yield current_block
			current_block = []
	if len(current_block) != 0:
		yield JsonMemoryStor(current_block)
		current_block = []



class DiskStor(Stor):
	"""
		Stor to manage data stored in a single file on disk.
		Notes:
			- _contents.setter: opens the file, saves filepath
			- _contents.deleter: closes file, deletes it
			- _filepath: location of file 
			- _blocksize: size of blocks during iteration

		Subclasses Implement:
		---------------------
		@contents.getter: should return an iterator over blocks
	"""

	def __init__(self, filepath, blocksize):
		super(DiskStor, self).__init__()
		self.set_contents(filepath)
		self.blocksize = blocksize


	#==========[ CONTENTS	]==========
	def set_contents(self, filepath):
		self._filepath = filepath
		self._contents = open(self._filepath, 'r')
	def del_contents(self):
		self._contents.close()
		os.remove(self._filepath)


	#==========[ APPLICATION	]==========
	def apply(self, operation):
		for block in self.contents:
			block.apply(operation)







################################################################################
####################[ JsonDiskStor ]############################################
################################################################################

class JsonDiskStor(DiskStor):
	"""
		Stor: JsonDiskStor
		--------------------
		Usage:
			stor = JsonDiskStor('/path/to/file')
		Description:
			Stor for data stored in a single, large json file.
			Assumes that each item ("event") is stored in the top-level
			list.
			recommendation: convert to JsonBlocksStor!
	"""
	def __init__(self, filepath, blocksize=10000):
		super(JsonDiskStor, self).__init__(filepath, blocksize)


	#==========[ CONTENTS	]==========
	def get_contents(self):
		item_gen = ijson.items(self._contents, 'item')
		for block in blocks_from_generator(item_gen, self.blocksize):
			yield JsonMemoryStor(block)









################################################################################
####################[ CsvDiskStor ]#############################################
################################################################################

class CsvDiskStor(DiskStor):
	"""
		Stor: CsvDiskStor
		--------------------
		Usage:
			stor = CsvDiskStor('/path/to/file')
		Description:
			Stor for data stored in a single, large csv file.
			stores it in a pandas dataframe
	"""
	def __init__(self, filepath, blocksize=10000, delimiter=','):
		super(CsvDiskStor, self).__init__(filepath, blocksize)
		self.delimiter =','

	
	#==========[ CONTENTS	]==========
	def get_contents(self):
		block_gen = pd.read_csv(self._filepath, chunksize=self.blocksize, delimiter=self.delimiter)
		for block in block_gen:
			yield PandasMemoryStor(block)


	def load_in_memory(self, nrows=None):
		"""
			loads contents into a pandas dataframe, self.df 
		"""
		return PandasMemoryStor(pd.read_csv(self.filepath, sep=self.delimiter, nrows=self.nrows))


