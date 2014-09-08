import json
import simplejson
import pandas as pd

from metapython.stor.Stor import *


class MemoryStor(Stor):
	"""
		Stor: MemoryStor
		----------------
		abstract Stor for those that store contents in memory
	"""
	def __init__(self, contents):
		super(MemoryStor, self).__init__()
		self._contents = contents



class JsonMemoryStor(MemoryStor):
	"""
		Stor: JsonMemoryStor
		----------------------
		Usage:
			stor = JsonMemoryStor(json.load(open('test.json', 'r')))
		Description:
			manages a block of json in memory 
	"""
	def __init__(self, contents):
		super(JsonMemoryStor, self).__init__(contents)
		assert type(self.get_contents()) == list


	def iter_items(self):
		for x in self.contents:
			yield x



class PandasMemoryStor(MemoryStor):
	"""
		Stor: PandasMemoryStor
		----------------------
		Usage:
			stor = PandasMemoryStor(json.load(open('test.json', 'r')))
		Description:
			manages a block of panas df in memory
	"""
	def __init__(self, contents):
		super(PandasMemoryStor, self).__init__(contents)
		assert type(self.get_contents()) == pd.DataFrame


	def iter_items(self):
		for row in self.contents.iterrows():
			yield row
