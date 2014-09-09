from copy import deepcopy
from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first
from lxml import etree

class SolvProblem(SearchProblem):

	################################################################################
	####################[ Interface for Op Scripts ]################################
	################################################################################

	def __init__(self, initial_state, goal_state, actions_list):
		super(SolvProblem, self).__init__(initial_state)
		self.goal_state = None
		self.actions_list = actions_list


	################################################################################
	####################[ Basic Methods for A* Search ]#############################
	################################################################################

	def apply_sites(self, state, action):
		"""
			returns the set of paths that action can apply itself to
		"""
		return action['xpath'](state)


	def action_applies(self, state, action):
		"""
			returns true if the action can apply to the current state
		"""
		return len(self.apply_sites(state, action)) > 0


	def actions(self, state):
		"""
			returns the list of actions you can take in current state 
				(this will be a list of Ops) 

			:todo: have a list of actions that are accessible to this, return all 
			that can actionerate on the current state
		"""
		actions = [action for action in self.actions_list if self.action_applies(state, action)]
		print "===[ ACTIONS ]==="
		for action in actions:
			print action['xpath']
		return actions



	def result(self, state, action):
		"""
			returns what happens when you apply an action in a certain state 
		"""
		state = deepcopy(state)
		print '#####[ APPLYING ACTION ]#####'
		print action['name']
		print action['xpath']
		print "			BEFORE: "
		print etree.tostring(state, pretty_print=True)
		originals = self.apply_sites(state, action)
		for original in originals:
			action['transformation'](original)
		print "			AFTER: "
		print etree.tostring(state, pretty_print=True)
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
		equal = elements_equal(state, goal_state)

		return elements_equal(state, goal_state)


	def cost(self, state, action, state2):
		"""
			returns the cost of applying action in state to get to state2
		"""
		return 1





if __name__ == '__main__':

	initial_state = etree.fromstring("""
<filesystem location="/data/">
	<dataframe>
		<column name="A" type="text" tokenized="False" stemmed="False" lowercased="False" />
		<column name="B" type="text" tokenized="False" stemmed="False" lowercased="False" />
		<column name="C" type="text" tokenized="False" stemmed="False" lowercased="False" />				
	</dataframe>
</filesystem>
""")

	goal_state = etree.fromstring("""
<filesystem location="/data/">
	<dataframe>
		<column name="A" type="text" tokenized="True" stemmed="True" lowercased="True" />
		<column name="B" type="text" tokenized="True" stemmed="True" lowercased="True" />
		<column name="C" type="text" tokenized="True" stemmed="True" lowercased="True" />				
	</dataframe>
</filesystem>
""")

	#=====[ Goal: tokenize and shit	]=====
	tokenize = {
					'xpath': etree.XPath('//dataframe/column[@type="text"][@tokenized="False"]'),
					'transformation': lambda x: x.set('tokenized', 'True'),
					'name':'tokenize'
	}
	lowercase = {
					'xpath': etree.XPath('//dataframe/column[@type="text"][@lowercased="False"]'),
					'transformation': lambda x: x.set('lowercased', 'True'),
					'name':'lowercase'
	}
	stem = {
					'xpath': etree.XPath('//dataframe/column[@type="text"][@stemmed="False"]'),
					'transformation': lambda x: x.set('stemmed', 'True'),
					'name':'stem'
	}
	solv = SolvProblem(initial_state, goal_state, [tokenize, lowercase, stem])
	result = breadth_first(solv)
















