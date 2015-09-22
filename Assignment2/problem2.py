from ga_abstract import GeneticAlgorithm

# Artificial Intelligence Assignment 2 Problem 2

class BinGA(GeneticAlgorithm):
    def __init__(self, traits):
        self.traits = list(traits)
        # initialize population
        pass

    def generatePopulation(self):
        pass

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
