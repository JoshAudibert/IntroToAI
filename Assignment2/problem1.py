import BaseGA from ga
import random

# Artificial Intelligence Assignment 2 Problem 3

class AddingGA(BaseGA):
	def __init__(self, goalVal):
		# initialize population
		self.goalVal = goalVal

	def fitnessFn(self, child):
		NEG_MULT = 2
		childSum = sum(child)
		if childSum > self.goalVal:
			return NEG_MULT * (childSum - self.goalVal)
		else:
			return self.goalVal - childSum

	def randomSelection(self, population, fitnessFn):
		# List of child, fitness pairs
		pop_fitnesses = [[child, fitnessFn(child)] for child in population]
		total = sum(pop_fitness[1] for pop_fitness in pop_fitnesses)
		rand = random.uniform(0, total)
		cumul_sum = 0
		# finds which fitness range the rand fell into
		for child, pop_fitness in pop_fitnesses:
			if rand < cumul_sum + pop_fitness:
				return child
			cumul_sum += pop_fitness


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
