from metaprogramming.op.Op import *
from metaprogramming.op.pandas_formatting import *
from metaprogramming.op.pandas_manipulation import *
from metaprogramming.op.decorators import *
from metaprogramming.stor.Stor import *
from metaprogramming.stor.DiskStor import *
from metaprogramming.stor.BlockStor import *
from metaprogramming.stor.MemoryStor import *
import matplotlib.pyplot as plt

disc_cols = ['sessionId', 'userId', 'A', 'F', 'C', 'country', 'gameBrand', 'gameType']
cont_cols = ['sessionId', 'userId', 'balance', 'bet', 'casinoLevel', 'gameSeq', 'lines', 'nCount']

shaker_pipeline = 	keep_columns(cols=list(set(disc_cols).union(set(cont_cols)))) +\
					split_columns(left_cols=cont_cols, right_cols=disc_cols) +\
					(split_by_key(key_col='sessionId') | split_by_key(key_col='sessionId'))




@op(num_out=1)
def plot_random_user_balance_sessions(dict_of_dfs, col):
	random_key = random.choice(dict_of_dfs.keys())
	df = dict_of_dfs[random_key]
	nonNan = df.ix[df[col].notnull()]
	sorted_df = nonNan.sort(columns=['_time'])
	plt.plot(sorted_df[col])
	plt.show()


simple_fuck_with_shaker = keep_columns(cols=['sessionId','userId','balance', 'bet', '_time']) + split_by_key(key_col='sessionId')

if __name__ == '__main__':

	demo_filepath = '/Users/jayhack/Desktop/shaker_data/demographics.csv'
	sessions_1_filepath = '/Users/jayhack/Desktop/shaker_data/sessions_1.csv'
	sessions_2_filepath = '/Users/jayhack/Desktop/shaker_data/sessions_2.csv'

	#=====[ Step 1: set up Stors	]=====
	dems = CsvDiskStor(demo_filepath)
	actions_stor_1 = CsvDiskStor(sessions_1_filepath)
	actions_stor_2 = CsvDiskStor(sessions_2_filepath)

	#=====[ Step 2: get a list of dataframes, one for each session	]=====
	actions_df = actions_stor_1.get_contents().next()._contents
	dfs = simple_fuck_with_shaker(actions_df)






