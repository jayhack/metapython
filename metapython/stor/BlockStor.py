import os
import sys

from metapython.stor.Stor import *
from metapython.stor.MemoryStor import *


class BlockStor(Stor):
	"""
		Stor: BlockStor
		---------------
		abstract Stor for those that store contents in blocks on disk
	"""
	def __init__(self, filepath=None):
		super(PandasBlockStor, self).__init__()
		assert os.path.isdir(filepath)
		self.filepath = filepath
		self.block_filepaths = self.get_block_filepaths ()


	def make_block_name(self):
		return os.path.join(self.filepath, 'block_%s' % str(time.time()))


	def get_block_filepaths(self):
		return [os.path.join(self.filepath, p) for p in os.listdir(self.filepath)]


	def clear(self):
		for filepath in self.block_filepaths:
			os.remove(filepath)
		self.block_filepaths = []
		return self


	def load_block(self, filepath):
		raise NotImplementedError


	def dump_block(self, filepath):
		raise NotImplementedError


	def add(self, memory_stor):
		self.dump_block(memory_stor, self.make_block_name())


	def iter_blocks(self):
		for filepath in self.block_filepaths:
			yield self.load_block(filepath)




class JsonBlocksStor(BlockStor):
	"""
		Stor: JsonBlocksStor
		--------------------
		Usage:
			stor = JsonBlocksStor('/path/to/blocks/directory')
		Description:
			Stor for data stored in large blocks of json on disk.
	"""
	def __init__(self, filepath=None):
		super(JsonBlocksStor, self).__init__(filepath)


	def load_block(self, filepath):
		return JsonMemoryStor(simplejson.load(open(filepath, 'r')))


	def dump_block(self, filepath):
		simplejson.dump(memory_stor, open(self.make_block_name(), 'w'), use_decimal=True)




class PandasBlocksStor(BlockStor):
	"""
		Stor: PandasBlocksStor
		--------------------
		Usage:
			stor = PandasBlocksStor('/path/to/blocks/directory')
		Description:
			Stor for data stored in large blocks of pandas dataframes on disk.
	"""
	def __init__(self, filepath=None):
		super(PandasBlocksStor, self).__init__(filepath)


	def load_block(self, filepath):
		return pd.read_pickle(filepath)


	def dump_block(self, filepath):
		memory_stor.to_pickle(filepath)
