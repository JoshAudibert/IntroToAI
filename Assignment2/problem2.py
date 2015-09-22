from ga_abstract import GeneticAlgorithm

# Artificial Intelligence Assignment 2 Problem 2


class BinGA(GeneticAlgorithm):
    def __init__(self, numList):
        # initialize population
        self.numList = numList
        
    def generatePopulation(self):
        pass

    def fitnessFn(self, child):
        pass

    def randomSelection(self, population, fitnessFn):
        pass

    def reproduce(self, parent_x, parent_y):
        pass

    def mutate(self, child):
        pass

    def str_phenotype(self, child):
                return self.filter_traits(child)
