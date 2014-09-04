import unittest
import nose

import os
import json
import pandas as pd

from DiskStor import *
from BlockStor import *
from MemoryStor import *



################################################################################
####################[ DISKSTOR ]################################################
################################################################################

class TestDiskStor(unittest.TestCase):

	def setUp(self):
		j = [{'foo':1}]*1000
		json.dump(j, open('temp.json','w'))
		pd.DataFrame([{'foo':1, 'bar':2}]*1000).to_csv('temp.df')

	def tearDown(self):
		if os.path.exists('./temp.json'):
			os.remove('temp.json')
		if os.path.exists('./temp.df'):
			os.remove('temp.df')



	def test_json_diskstor_basic(self):
		stor = JsonDiskStor('temp.json', blocksize=100)
		for block in stor.get_contents():
			self.assertEquals(len(block._contents), 100)

	def test_json_diskstor_clear(self):
		stor = CsvDiskStor('temp.df', blocksize=100)
		stor.clear()
		self.assertFalse(os.path.exists('./temp.df'))


	def test_csv_diskstor_basic(self):
		stor = CsvDiskStor('temp.df', blocksize=100)
		for block in stor.get_contents():
			self.assertEquals(len(block._contents), 100)

	def test_csv_diskstor_clear(self):
		stor = CsvDiskStor('temp.df', blocksize=100)
		stor.clear()
		self.assertFalse(os.path.exists('./temp.df'))





################################################################################
####################[ BLOCKSTOR ]###############################################
################################################################################

class TestBlockStor(unittest.TestCase):

	def setUp(self):
		j = [{'foo':1}]*1000
		json.dump(j, open('temp.json','w'))
		pd.DataFrame([{'foo':1, 'bar':2}]*1000).to_csv('temp.df')
		self.json_diskstor = JsonDiskStor('temp.json', blocksize=100)
		self.csv_diskstor = CsvDiskStor('temp.json', blocksize=100)

	def tearDown(self):
		pass


	def test_json_blockstore(self):
		pass

