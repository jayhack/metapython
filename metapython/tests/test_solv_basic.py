import os
import unittest 
import nose
from lxml import etree

from metapython.solv.Solv import *

################################################################################
####################[ available actions/ops ]###################################
################################################################################
# Step 1: load the flat csvs into memory
load_flat_csv = {
	'name': 'load_flat_csv',
	'targets': '//filesystem[@type="local_disk"]/file_resource[@type="flat_file"][@format="csv"]',
	'transformation': lambda x: x.set('type', 'in_memory')
}

# Step 2: lowercase them
lowercase = {
	'name':'lowercase',
	'targets': '//filesystem[@type="local_disk"]/file_resource[@type="in_memory"]/column[@type="text"][@lowercased="False"]',
	'transformation': lambda x: x.set('lowercased', 'True')
}

# Step 3: in-memory to blocks
def imtb(node):
	node.set('type', 'blocks')
	node.set('location', './solvdata')
in_memory_to_blocks = {
	'name': 'in_memory_to_blocks',
	'targets': '//filesystem[@type="local_disk"]/file_resource[@type="in_memory"]',
	'transformation': imtb
}

# Step 4: combine blocks (totally naive)
combine_blocks = {
	'name': 'combine_blocks',
	'targets': '//filesystem[count(file_resource[@type="flat_file"]) >= 2]',
	'transformation': lambda node: node.remove(node.getchildren()[0])
}


state = etree.fromstring("""
<root>
	<a />
	<b>
		<c />
	</b>
</root>""")

#Goal: go from two csv files to a tokenized version that combines them into blocks
INITIAL_STATE = etree.fromstring("""
<root>
	<filesystem type="local_disk" path="/Users/jayhack/Desktop/205/Shaker/data">
		<file_resource type="flat_file" format="csv" location="sessions_1.csv">
			<column name="sessionId" type="int" />
			<column name="A" type="text" tokenized="False" lowercased="False" />
			<column name="F" type="text" tokenized="False" lowercased="False" />
			<column name="C" type="text" tokenized="False" lowercased="False" />
		</file_resource>
		<file_resource type="flat_file" format="csv" location="sessions_2.csv">
			<column name="A" type="text" tokenized="False" lowercased="False" />
			<column name="F" type="text" tokenized="False" lowercased="False" />
			<column name="C" type="text" tokenized="False" lowercased="False" />
		</file_resource>
	</filesystem>
</root>
""")

GOAL_STATE = etree.fromstring("""
<root>
	<filesystem location="%s">
		<file_resource type="blocks" format="csv" location="./solvdata">
			<column name="A" type="text" lowercased="True">
			<column name="F" type="text" lowercased="True">
		</file_resource>
	</filesystem>
</root>
""" % os.getcwd())


class Test_solv_basic(unittest.TestCase):

	def setUp(self):
		if os.path.exists('./solvdata'):
			os.rmdir('./solvdata')
		os.mkdir('./data')

	def tearDown(self):
		if os.path.exists('./solvdata'):
			os.rmdir('./solvdata')


	def test_basic(self):
		solv = SolvProblem(INITIAL_STATE, GOAL_STATE, [load_flat_csv, lowercase, in_memory_to_blocks, combine_blocks])
		result = breadth_first(solv)
		print [action['name'] for action in result.path() if ['name'] in action]





