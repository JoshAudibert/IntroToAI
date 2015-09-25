import abc
from ga_abstract import GeneticAlgorithm
import random

# Artificial Intelligence Assignment 2 Problem 1

class AddingGA(GeneticAlgorithm):
    def __init__(self, goalVal, traits):
        # initialize population
        self.POP_SIZE = 10
        self.goalVal = goalVal
        self.traits = list(traits)

    def generatePopulation(self):
        population = []
        for i in range(self.POP_SIZE):
            individual = []
            for j in range(len(self.traits)):
                if random.randint(0, 1):
                    individual.append(1)
                else:
                    individual.append(0)
            population.append(individual)
        return population

    def fitnessFn(self, child):
        NEG_MULT = 2
        childSum = sum(self.filter_traits(child))
        if childSum > self.goalVal:
            return NEG_MULT * (childSum - self.goalVal)
        else:
            return self.goalVal - childSum

    # return the list of numbers that the child represents
    def filter_traits(self, child):
        filtered = []
        for i in range(len(self.traits)):
            if child[i]:
                filtered.append(self.traits[i])

        return filtered

    # choosed a single parent from the population to reproduce with a weighted probability
    # based on the fitnesses of each child
    def randomSelection(self, population, fitnessFn):
        # List of child, fitness pairs
        pop_fitnesses = [[child, fitnessFn(child)] for child in population]
        
        # TODO: maybe put this into the fitnessFn
        max_fit = max([fitness for child, fitness in pop_fitnesses])
        norm_fitnesses = [[child, (-1) * fitness + max_fit + 1] for child, fitness in pop_fitnesses]

        total = sum(pop_fitness[1] for pop_fitness in norm_fitnesses)
        rand = random.uniform(0, total)
        cumul_sum = 0
        # finds which fitness range the rand fell into
        for child, pop_fitness in norm_fitnesses:
            if rand < cumul_sum + pop_fitness:
                return child
            cumul_sum += pop_fitness

    # splits the parent lists at a random point and combines their halves to form two children
    # returns one of these children
    def reproduce(self, parent_x, parent_y):
        # generate a split index
        split = random.randint(1, len(parent_x) - 1)

        # generate the sub-lists from the split
        x_left = list(parent_x[0:split])
        x_right = list(parent_x[split:])
        y_left = list(parent_y[0:split])
        y_right = list(parent_y[split:])

        # merge the sub-lists to create children
        child_a = x_left + y_right
        child_b = y_left + x_right

        # TODO: we may want to add a flag to potentially return both children
        return child_a

    # flips a random input integer from on or off
    def mutate(self, child):
        flip = random.randint(0, len(child)-1)
        if child[flip] == 1:
            child[flip] = 0
        else:
            child[flip] = 1
        return child

    # returns the list of numbers that represents the child
    def str_phenotype(self, child):
        return self.filter_traits(child)
        
    def cull(self, population, num_cull):
        sorted_pop = sorted(population, key = self.fitnessFn)
        for i in range(num_cull):
            population.remove(sorted_pop[len(sorted_pop) - 1 - i])
            
    def getElites(self, population, num_elite):
        sorted_pop = sorted(population, key = self.score)
        elites = []
        for i in range(num_elite):
            elites.append(sorted_pop[-i])
        return elites

    def score(self, child):
        total = sum(self.filter_traits(child))
        if total > self.goalVal:
            return 0
        return total


