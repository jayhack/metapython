# import numpy as np
# import pandas as pd

# from metapython.op.Op import *


# '''
# 	Op: get_dummies
# 	------------------
# 	usage:
# 		df = get_dummies(df)
# 	description:
# 		given a df that consists of only columns that are labels 
# 		(i.e. take on discrete values, like 'Male'/'Female'), this 
# 		returns a new df that has converted it to one-hot representations,
# 		though *not* with the same column names!
# '''
# get_dummies = Op([
# 	(1, 1, '''lambda df: pd.concat([pd.get_dummies(df[col]) for col in df.columns], axis=1)''')
# ])



# '''
# 	Op: featurize_labels
# 	-----------------------
# 	usage:
# 		df = featurize_labels(cols=['a','b'])(df)
# 	params:
# 		- cols: columns containing labels
# 	description:
# 		given a dataframe with certain columns containing labels,
# 		this will return a new df with those labels featurized
# '''



# '''
# featurize_session_continuous

# given a 'session', represented as a numpy array of shape (num_observations, num_features), featurizes into the average of the last n observations
# '''

# featurize_session_continuous= Op([
# (1, 1, '''lambda matrix: np.average(matrix[-{n}:], axis=0)''')

# ])


# '''
# featurize_session_discrete

# given a 'session', represented as a numpy array of shape (num_observations, num_feature), featurizes into the concatenation of the last n observations
# '''
# featurize_session_discrete = Op([
# 	(1, 1, '''lambda matrix: matrix[-{n}:].flatten()''')

# 	])

# '''
# generate_samples_from_continuous_session

# given a session, returns an sklearn-like X and y array that has positive and negative examples. Note that this assumes that the session's only "positive" example is at the end (i.e shaker). looks at n-length windows.

# params:
# 	-n: length of windows
# '''



# generate_samples_from_continuous_session = Mop(1,2,'''mat
# 													X = np.array([np.average(mat[:end][-{n}:], axis=0) for end in range({n}, len(mat)+1)])
# 													y = np.array([1 if end==len(mat) else 0 for end in range({n}, len(mat)+1)])
# 													return X, y''')

# # generate_samples_from_continuous_session = Op([
# # (1, 2, '''lambda mat: (np.array([np.average(mat[:end][-{n}:], axis=0) for end in range({n}, len(mat)+1)]), np.array([1 if end==len(mat) else 0 for end in range({n}, len(mat)+1)]))''')




# # 	])


# '''
# generate_samples_from_discrete_session

# given a session, returns an sklearn-like X and y array that has positive and negative examples. Note that this assumes that the session's only "positive" example is at the end (i.e shaker). looks at n-length windows.

# params:
# 	-n: length of windows
# '''


# generate_samples_from_discrete_session = Op([
# (1, 2, '''lambda mat: (np.array([mat[:end][-{n}:].flatten() for end in range({n}, len(mat)+1)]), np.array([1 if end==len(mat) else 0 for end in range({n}, len(mat)+1)]))''')




# 	])



# '''
# list_of_featurized_vectors_to_X

# given a list of featurized vectors, returns a sk-learn type "X" matrix, with shape (n_samples, n_features)


# '''
# list_of_featurized_vectors_to_x = Op([
# 	(1, 1, '''lambda list_of_featurized_vectors: np.array(list_of_Featurized_vectors)''')
# 	])





