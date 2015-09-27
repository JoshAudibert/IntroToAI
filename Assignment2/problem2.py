from ga_abstract import GeneticAlgorithm
import random

# Artificial Intelligence Assignment 2 Problem 2


class BinGA(GeneticAlgorithm):

    def __init__(self, traits):
        self.POP_SIZE = 5
        self.MUTATION_PROB = .05
        self.traits = list(traits)

    def binCheck(self, child):
        bc_one = 0
        bc_two = 0
        bc_three = 0
        bin_size = int(len(child)/3.0)
        for i in range(len(child)):
            if child[i] == 1:
                if bc_one < bin_size:
                    bc_one += 1
                else:
                    if bc_two < bin_size:
                        child[i] = 2
                        bc_two += 1
                    else:
                        child[i] = 3
                        bc_three += 1
            elif child[i] == 2:
                if bc_two < bin_size:
                    bc_two += 1
                else:
                    if bc_one < bin_size:
                        child[i] = 1
                        bc_one += 1
                    else:
                        child[i] = 3
                        bc_three += 1
            else:
                if bc_three < bin_size:
                    bc_three += 1
                else:
                    if bc_one < bin_size:
                        child[i] = 1
                        bc_one += 1
                    else:
                        child[i] = 2
                        bc_two += 1

        return child

    def generatePopulation(self):
        population = []
        for i in range(self.POP_SIZE):
            individual = []
            for j in range(len(self.traits)):
                individual.append(random.randint(1,3))
            individual = self.binCheck(individual)
            population.append(individual)
        return population

    def fitnessFn(self, child):
        return self.score(child)

    # return the list of numbers that the child represents
    def filter_traits(self, child):
        filtered = []
        for i in range(len(self.traits)):
            filtered.append([self.traits[i], child[i]])

        return filtered

    def randomSelection(self, population):
        # List of child, fitness pairs
        pop_fitnesses = [[child, self.fitnessFn(child)] for child in population]
        # since fitness can be negative, need to make things positive for weighted
        # probability
        min_fit = abs(min([fitness for child, fitness in pop_fitnesses]))
        norm_fitnesses = [[child, fitness + min_fit + 1] for child, fitness in pop_fitnesses]
        total = sum(fitness for child, fitness in norm_fitnesses)
        rand = random.uniform(0, total)
        cumul_sum = 0
        # finds which fitness range the rand fell into
        for child, fitness in norm_fitnesses:
            if rand < cumul_sum + fitness:
                return child
            cumul_sum += fitness

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

        better_childa = self.binCheck(child_a)
        better_childb = self.binCheck(child_b)
        return better_childa

    def mutate(self, child):
        flipOne = random.randint(0,len(child)-1)
        flipTwo = random.randint(0,len(child)-1)
        while child[flipOne] == child[flipTwo]:
            flipTwo = random.randint(0,len(child)-1)
        child[flipOne], child[flipTwo] = child[flipTwo], child[flipOne]

        return child

    def str_phenotype(self, child):
        return "%s\nFitness: %s" % (str(self.filter_traits(child)), self.fitnessFn(child))
        
    def cull(self, population, num_cull):
        sorted_pop = sorted(population, key = self.fitnessFn)
        for i in range(num_cull):
            population.remove(sorted_pop[i])
            
    def getElites(self, population, num_elite):
        sorted_pop = sorted(population, key = self.score)
        elites = []
        for i in range(num_elite):
            elites.append(sorted_pop[-i])
        return elites

    def score(self, child):
        b_one = 1
        b_two = 0
        for i in range(len(child)):
            if child[i] == 1:
                b_one *= self.traits[i]
            elif child[i] == 2:
                b_two += self.traits[i]
        return b_one + b_two

