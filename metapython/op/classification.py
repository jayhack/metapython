'''
multinomial_naive_bayes

given an "X" matrix of shape (n_samples, n_features), returns a fitted sklearn multinomial naive bayes object
'''

multinomial_naive_bayes = Op([
(2, 1, 'lambda X, y: MultinomialNaiveBayes().fit(X, y)') # should return the mnb according to docs, but check!

	])

'''
gaussian_naive_bayes

given an "X" matrix of shape (n_samples, n_features), returns a fitted sklearn multinomial naive bayes object
'''
gaussian_naive_bayes = Op([
(2, 1, 'lambda X,y: GaussianNaiveBayes().fit(X, y)')

	])