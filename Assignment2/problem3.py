from ga_abstract import GeneticAlgorithm
import random

# Artificial Intelligence Assignment 2 Problem 3

# class that holds the piece information
class towerPiece:
    def __init__(self, pieceType, width, strength, cost):
        self.pieceType = pieceType
        self.width = width
        self.strength = strength 
        self.cost = cost 

    def __str__(self):
        return "%s, %d, %d, %d" % (self.pieceType, self.width, self.strength, self.cost)

# Genetic algorithm to solve problem 3 (Tower Building Problem)
class TowerGA(GeneticAlgorithm):
    def __init__(self, pieces):
        # contains probability of mutation occuring, the desired population
        # size and the list of all of the original tower pieces
        self.MUTATION_PROB = .05
        self.POP_SIZE = 15
        self.pieces = list(pieces)

    # Determine if there are two pieces at the same level
    # and turn one piece off it a piece is alread present there
    def checkTower(self, child):
        checkList = [0] * (len(self.pieces) + 1)
        for i in range(len(child)):
            if child[i]:
                if checkList[child[i]]:
                    child[i] = 0
                else:
                    checkList[child[i]] = 1
        return child

    # Generate the initial population of size POP_SIZE
    def generatePopulation(self):
        population = []
        piece_used = [0] * len(self.pieces)
        while len(population) < self.POP_SIZE:
            tower_size = random.randint(1,len(self.pieces))
            tower = [0] * len(self.pieces)
            pieces_left = [1] * len(self.pieces)
            for i in range(1, tower_size+1): # from 1 to tower_size
                next_piece = 0
                while next_piece == 0:
                    next_index = random.randint(0,len(self.pieces)-1)
                    next_piece = pieces_left[next_index]
                    pieces_left[next_index] = 0
                tower[next_index] = i
                piece_used[i-1] = 1

            if len(population) != self.POP_SIZE-1 or sum(piece_used) == len(self.pieces):
                population.append(tower)

        return population
    # Fitness function evaluated as (10 + 2**(height of tower -
    # (total cost of pieces used))** .75*(number of rules broken)
    def fitnessFn(self, child):
        if child.count(0) == len(child):
            return 0
        # determine the number of rules broken
        num_broken_rules = self.countBrokenRules(child)
        num_pieces = 0
        tower_cost = 0
        for i in range(len(child)):
            if child[i]:
                num_pieces += 1
                tower_cost += self.pieces[i].cost
                
        fitness = 10 + (num_pieces*num_pieces) - tower_cost
        # scale it down by 3/4 for each rule broken
        fitness *= 0.75**num_broken_rules
        return fitness

    # return the piece that the child represents
    def filter_traits(self, child):
        tower = [0] * len(self.pieces)
        for i in range(len(child)):
            if child[i]:
                tower[child[i]-1] = str(self.pieces[i])
        # remove zeros
        tower = filter(lambda z: z != 0, tower)
        return tower

    # chooses a random parent to use to reproduce a child
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

    # generate a child by taking portions of the two parents
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

        better_child_a = self.checkTower(child_a)
        better_child_b = self.checkTower(child_b)

        return better_child_a

    # mutate by flipping a random piece in a child
    def mutate(self, child):
        flip = random.randint(0, len(child)-1)
        if child[flip]:
            child[flip] = 0
        else:
            child[flip] = random.randint(1, len(self.pieces))
            child = self.checkTower(child)
        return child

    # returns the list of numbers that represents the child
    def str_phenotype(self, child):
            return self.filter_traits(child)

    # Returns the number of rules broken by the current tower configuration
    def countBrokenRules(self, child):
        num_broken_rules = 0

        # build tower
        tower = [0] * len(self.pieces)
        for i in range(len(child)):
            if child[i]:
                tower[child[i]-1] = self.pieces[i]
        
        # remove zeros
        tower = filter(lambda z: z != 0, tower)

        if len(tower) == 0:
            return 2
        
        # check bottom for door
        if tower[0].pieceType != "Door":
            num_broken_rules += 1
            
        # check top for lookout
        if tower[-1].pieceType != "Lookout":
            num_broken_rules += 1
            
        # check middle for walls
        for i in range(1, len(tower)-1):
            if tower[i].pieceType != "Wall":
                num_broken_rules += 1
                
        # check widths of tower pieces
        current_width = tower[0].width
        for i in range(1, len(tower)):
            if tower[i].width <= current_width:
                current_width = tower[i].width
            else:
                num_broken_rules += 1
                
        # check strengths
        for i in range(len(tower)):
            if (len(tower)-1 - i) > tower[i].strength:
                num_broken_rules += 1

        return num_broken_rules
        
    # removes num_cull items from the population with the worst fitness function score
    def cull(self, population, num_cull):
        sorted_pop = sorted(population, key = self.fitnessFn)
        for i in range(num_cull):
            population.remove(sorted_pop[i])
           
    # returns num_elites of population with the best score
    def getElites(self, population, num_elite):
        # sort population based on score
        sorted_pop = sorted(population, key = self.score)
        elites = []
        # take items with top score
        for i in range(num_elite):
            elites.append(sorted_pop[-i])
        return elites

    # Score is evaluated as (10 + (height of tower)*2 - the total cost of the pieces used
    # If any rules are broken then the score is returned as zero
    def score(self, child):    
        num_broken_rules = self.countBrokenRules(child)
        if num_broken_rules > 0:
            return 0
            
        num_pieces = 0
        tower_cost = 0
        for i in range(len(child)):
            if child[i]:
                num_pieces += 1
                tower_cost += self.pieces[i].cost

        score = 10 + (num_pieces**2) - tower_cost
        return score
