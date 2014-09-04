from setuptools import setup, find_packages

setup(
		name='metapython',
		version='0.0.1',
		author="Jay Hack",
		author_email="jhack@stanford.edu",
		description="a utility for rapidly prototyping data scientific pipelines",
		packages=find_packages(),
		include_package_data=True,
		install_requires=[
			'numpy',
			'scipy',
			'pandas',
			'lazy_format',
			'scikit-learn',
			'gensim',
			'nltk',
			'simplejson',
			'ijson',
			'nose',
		]#,namespace_packages=['metapython']
)

