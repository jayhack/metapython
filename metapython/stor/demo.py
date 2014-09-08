import simplejson

from metaprogramming.stor.Stor import *

if __name__ == '__main__':

	acitivities_filepath = '/Users/jayhack/Desktop/205/SpotOn/data/activities/raw/activities_all.json'

	a_stor_raw = LargeJsonFileStor(filepath=acitivities_filepath)

	def dump_json(x, filename='test.json'): 
		simplejson.dump(x, open(filename, 'w'), use_decimal=True)

	activities_raw_stor.apply(dump_json)



