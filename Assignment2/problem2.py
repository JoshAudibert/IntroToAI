from ga_abstract import GeneticAlgorithm
import random

# Artificial Intelligence Assignment 2 Problem 2


class BinGA(GeneticAlgorithm):
    def __init__(self, traits):
        self.traits = list(traits)

    def binCheck(self, child):
        bc_one = 0
        bc_two = 0
        bc_three = 0
        for i in range(len(child)):
            if child[i] == 1:
                if bc_one < 10:
                    bc_one += 1
                else:
                    if bc_two < 10:
                        child[i] = 2
                        bc_two += 1
                    else:
                        child[i] = 3
                        bc_three += 1
            elif child[i] == 2:
                if bc_two < 10:
                    bc_two += 1
                else:
                    if bc_one < 10:
                        child[i] = 1
                        bc_one += 1
                    else:
                        child[i] = 3
                        bc_three += 1
            else:
                if bc_three < 10:
                    bc_three += 1
                else:
                    if bc_one < 10:
                        child[i] = 1
                        bc_one += 1
                    else:
                        child[i] = 2
                        bc_two += 1



    def generatePopulation(self):
        POP_SIZE = 20
        population = []
        for i in range(POP_SIZE):
            individual = []
            for j in range(len(self.traits)):
                individual.append(random.randint(1,2,3))
            population.append(individual)
            self.binCheck(self, population)
        return population

    def fitnessFn(self, child):
        b_one = 1
        b_two = 0
        for i in range(len(child)):
            if child[i] == 1:
                b_one *= self.traits[i]
            elif child[i] == 2:
                b_two += self.traits[i]
        return sum(b_one, b_two)

    def randomSelection(self, population, fitnessFn):
        pass

    def reproduce(self, parent_x, parent_y):
        pass

    def mutate(self, child):
        pass

    def str_phenotype(self, child):
        return self.filter_traits(child)
