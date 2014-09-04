import json
import simplejson
import ijson
import pickle
import pandas as pd


class Stor(object):
	"""
		Ideal Operation:
			stor1 = S3Stor(	
							bucket='s3://...',
							aw_access_key='...',
							aws_secret_key='...',
						)
			stor2 = LargeJsonStor('/path/to/single/file')
			stor3 = JsonBlocksStor('/path/to/directory/of/blocks')
			stor4 = SplunkStor(credentials='...')

			data_transform_op = PullS3ToJson + LargeJsonToBlocks
			data_transform_op(stor1, stor2, stor3)

	"""
	def __init__(self):
		self._contents = None
		self._load_code = None
		


	#==========[ CONTENTS	]==========
	def get_contents(self):
		return self._contents
	def set_contents(self, value):
		self._contents = value
	def del_contents(self):
		del self._contents


	def clear(self):
		"""
			remove this Stor's content from the face of 
			the earth
		"""
		self.del_contents()


	def describe(self):
		"""
			returns a description of this Stor, without 
			necessarily loading all contents into memory.
			Primarily for debugging?
		"""
		raise NotImplementedError


	def __ladd__(self, op):
		"""
			Adds this stor to an Op; does so by inserting 
			an Op with zero input that returns this one's output
		"""
		return 


