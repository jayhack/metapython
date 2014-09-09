################################################################################
####################[ OpRunner: Run Ops as scripts ]############################
################################################################################


from optparse import OptionParser
import os

from metapython.op.Op import *
from metapython.op.pandas_util import *
from metapython.op.std import *


parser = OptionParser()
parser.add_option("-i", "--infile",
		action="store", type="string", dest="infile", default="input.csv",
		help="specify the path to the input")
parser.add_option("-o", "--outfile",
		action="store", type="string", dest="outfile", default="output.csv",
		help="specify the path to the output")
parser.add_option("-n", "--op-name",
		action="store", type="string", dest="op_name", default="",
		help="specify the name of the operation to apply")

(options, args) = parser.parse_args()

infile  = options.infile
outfile = options.outfile
op_name = options.op_name


if hasattr(metapython.op.Op, op_name):
	op = getattr(metapython.op.Op, op_name)
elif hasattr(metapython.op.std, op_name) 
	op = getattr(metapython.op.std, op_name) 
elif hasattr(metapython.op.pandas_util, op_name)
	op = getattr(metapython.op.pandas_util, op_name)
else raise Exception("Op not found")


if os.path.exists(infile):
	with open(infile, 'rb') as input_file:
		"""
		read csv and put it into the op
		"""











