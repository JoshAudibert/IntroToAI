import BaseGA from ga

# Artificial Intelligence Assignment 2 Problem 3

class AddingGA(BaseGA):
	def __init__(self):
		# initialize population

	def fitnessFn(self, child):
		pass

	def randomSelection(self, population):
		pass

	def reproduce(self, parent_x, parent_y):
		# generate a split index
		split = random.randint(1, len(parent_x) - 1)
		
		# generate the sub-lists from the split
		x_left = list(parent_x[0:split-1])
		x_right = list(parent_x[split:])
		y_left = list(parent_y[0:split-1])
		y_right = list(parent_y[split:])
		
		# merge the sublists to create children
		child_a = x_left + y_right
		child_b = y_left + x_right
		
		# return something...
		
		pass

	def mutate(self, child):
		pass
