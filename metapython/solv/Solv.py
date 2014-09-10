import copy
from simpleai.search import SearchProblem
from simpleai.search.traditional import depth_first
from lxml import etree

class SolvProblem(SearchProblem):
	"""
		Spec:

			States: etree.ElementTree containing state
			Actions: (op, target)
				op - operation to be applied
				target_path - xpath to where we will apply it


	"""

	def __init__(self, initial_state, goal_state, ops_list, verbose=False):
		super(SolvProblem, self).__init__(initial_state)
		self.verbose = verbose

		self.goal_state = None
		self.ops_list = ops_list


	def get_target_paths(self, state, op):
		"""
			returns all nodes in state's "tree" to which op can bind
		"""
		nodes = state.xpath(op['targets'])
		paths = [state.getpath(n) for n in nodes]
		return paths


	def actions(self, state):
		"""
			returns all (target_path, transformation) pairs that apply to 
			the current state
		"""
		if self.verbose:
			print "=====[ ACTIONS ]====="
			print etree.tostring(state)
			print [(op, tp) for op in self.ops_list for tp in self.get_target_paths(state, op)]

		return [(op, tp) for op in self.ops_list for tp in self.get_target_paths(state, op)]



	def result(self, state, action):
		"""
			returns what happens when you apply an action in a certain state 
		"""
		state = copy.deepcopy(state)
		op, target_path = action
		target = state.xpath(target_path)[0]
		op['transformation'](target)
		return state


	def is_goal(self, state):
		"""
			true if you reached the goal state 
		"""
		def elements_equal(e1, e2):
			if e1.tag != e1.tag: return False
			if e1.text != e2.text: return False
			if e1.tail != e2.tail: return False
			if e1.attrib != e2.attrib: return False
			if len(e1) != len(e2): return False
			return all([elements_equal(c1, c2) for c1, c2 in zip(e1, e2)])

		return elements_equal(state.getroot(), goal_state.getroot())


	def cost(self, state, action, state2):
		"""
			returns the cost of applying action in state to get to state2
		"""
		return 1





if __name__ == '__main__':

	initial_state = etree.ElementTree(etree.fromstring("""
<filesystem location="/data/">
	<dataframe>
		<column name="A" type="text" tokenized="False" stemmed="False" lowercased="False" />
		<column name="B" type="text" tokenized="False" stemmed="False" lowercased="False" />
		<column name="C" type="text" tokenized="False" stemmed="False" lowercased="False" />				
	</dataframe>
</filesystem>
"""))

	goal_state = etree.ElementTree(etree.fromstring("""
<filesystem location="/data/">
	<dataframe>
		<column name="A" type="text" tokenized="True" stemmed="True" lowercased="True" />
		<column name="B" type="text" tokenized="True" stemmed="True" lowercased="True" />
		<column name="C" type="text" tokenized="True" stemmed="True" lowercased="True" />				
	</dataframe>
</filesystem>
"""))

	#=====[ Goal: tokenize and shit	]=====
	tokenize = {
					'targets':'//dataframe/column[@type="text"][@tokenized="False"]',
					'transformation': lambda x: x.set('tokenized', 'True'),
					'name':'tokenize'
	}
	lowercase = {
					'targets':'//dataframe/column[@type="text"][@lowercased="False"]',
					'transformation': lambda x: x.set('lowercased', 'True'),
					'name':'lowercase'
	}
	stem = {
					'targets':'//dataframe/column[@type="text"][@stemmed="False"]',
					'transformation': lambda x: x.set('stemmed', 'True'),
					'name':'stem'
	}
	solv = SolvProblem(initial_state, goal_state, [tokenize, lowercase, stem], verbose=True)
	result = depth_first(solv)
















