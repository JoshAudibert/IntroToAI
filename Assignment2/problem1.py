import abc
from ga_abstract import GeneticAlgorithm
import random

# Artificial Intelligence Assignment 2 Problem 3

class AddingGA(GeneticAlgorithm):
	def __init__(self, goalVal, traits):
		# initialize population
		self.goalVal = goalVal
		self.traits = list(traits)
		
	def generatePopulation(self):
		POP_SIZE = 20
		population = []
		for i in range(POP_SIZE):
			individual = []
			for j in range(len(self.traits)):
				if random.randint(0,1):
					individual.append(self.traits[j])
				else:
					individual.append(0)
			population.append(individual)
		return population

	def fitnessFn(self, child):
		NEG_MULT = 2
		childSum = sum(child)
		if childSum > self.goalVal:
			return NEG_MULT * (childSum - self.goalVal)
		else:
			return self.goalVal - childSum

	def randomSelection(self, population, fitnessFn):
		# List of child, fitness pairs
		for child in population:
			if(type(child) != list):
				print "problem"
				print child
		
		pop_fitnesses = [[child, fitnessFn(child)] for child in population]
		max_fit = -1
		for fitness in pop_fitnesses:
			if fitness[1] > max_fit:
				max_fit = fitness[1]
		norm_fitnesses = [[pop_fitness[0], (-1) * pop_fitness[1] + max_fit + 1] for pop_fitness in pop_fitnesses]
		total = sum(pop_fitness[1] for pop_fitness in norm_fitnesses)
		rand = random.uniform(0, total)
		cumul_sum = 0
		# finds which fitness range the rand fell into
		for child, pop_fitness in norm_fitnesses:
			if rand < cumul_sum + pop_fitness:
				return child
			cumul_sum += pop_fitness


	def reproduce(self, parent_x, parent_y):
		# generate a split index
		#print len(parent_x)
		split = random.randint(1, len(parent_x) - 1)
		
		# generate the sub-lists from the split
		x_left = list(parent_x[0:split])
		x_right = list(parent_x[split:])
		y_left = list(parent_y[0:split])
		y_right = list(parent_y[split:])
		
		# merge the sublists to create children
		child_a = x_left + y_right
		child_b = y_left + x_right
		
		# return something...
		if(len(child_a) != 4):
			print child_a
		return child_a
		
		pass

	def mutate(self, child):
		pass
