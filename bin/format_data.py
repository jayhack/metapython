from metaprogramming.op.Op import *
from metaprogramming.stor.Stor import *
from metaprogramming.stor.DiskStor import *
from metaprogramming.stor.BlockStor import *

# operats on Stors, all of which should implement the "clear" method
clear_stor = Op([
	(1, 1, '''lambda x: x.clear ()''')
])


'''
	Op: disk_to_blocks
	------------------
	params:
		- disk_stor: JsonDiskStor for json files 
		- block_stor: JsonBlockStor for json files

	given a DiskStor an a BlocksStor, takes contents 
	of one and stores it in the other 

'''
disk_to_blocks = Op([
	(2, 1, '''lambda disk_stor, blocks_stor: disk_stor.apply_blocks(blocks_stor.add)''')
])


if __name__ == '__main__':

	a_disk_path = '/Users/jayhack/Desktop/205/SpotOn/data/activities/raw/activities_all.json'
	a_blocks_path = '/Users/jayhack/Desktop/205/SpotOn/data/activities/blocks_temp/'
	a_disk = JsonDiskStor(filepath=a_disk_path)
	a_blocks = JsonBlocksStor(filepath=a_blocks_path)

	transfer_data = (identity_op | clear_stor) +\
					single_file_to_blocks

	transfer_data(a_disk, a_blocks)


