from ga_abstract import GeneticAlgorithm
import random

# Artificial Intelligence Assignment 2 Problem 3

# class that holds the map information
class towerPiece:
    def __init__(self, pieceType, width, strength, cost):
        self.pieceType = pieceType
        self.width = width
        self.strength = strength 
        self.cost = cost 

class TowerGA(GeneticAlgorithm):
    def __init__(self, pieces):
        # initialize population
        self.pieces = list(pieces)

    def generatePopulation(self):
        POP_SIZE = 20
        population = []
        while(len(population) < POP_SIZE):
            tower_size = random.randint(1,len(self.pieces))
            tower = [0 for x in range(len(self.pieces))]
            pieces_left = [1 for x in range(len(self.pieces))]
            for i in range(tower_size):
                next_piece = 0
                while next_piece == 0:
                    next_index = random.randint(0,len(self.pieces)-1)
                    next_piece = pieces_left[next_index]
                    pieces_left[next_index] = 0
                tower[next_index] = i
            population.append(tower)
        return population
    
    def fitnessFn(self, child):
        num_pieces = 0
        tower_cost = 0
        for i in range(len(child)):
            if child[i] > 0:
                num_pieces = num_pieces + 1
                tower_cost = tower_cost + self.pieces[i].cost
        # score assuming no violations
        base_score = num_pieces * num_pieces - tower_cost
        
        tower = [0 for x in range(num_pieces)]
        for i in range(len(child)):
            if child[i] > 0:
                tower[child[i]] = self.pieces[i]
        
        for i in range(len(tower)):
            if tower[i] == 0:
                tower.pop(i)
                
        fitness_score = base_score
        
        # check bottom for door
        if tower[0].pieceType != "door":
            fitness_score = 0.75 * fitness_score
            
        # check top for lookout
        if tower[len(tower) - 1].pieceType != "lookout":
            fitness_score = 0.75 * fitness_score
            
        # check middle for walls
        for i in range(1, len(tower) - 1):
            if tower[i].pieceType != "wall":
                fitness_score = 0.75 * fitness_score
                
        # check widths of tower pieces
        current_width = tower[0].width
        for i in range(1, len(tower)):
            if tower[i].width < current_width:
                current_width = tower[i].width
            elif tower[i].width > current_width:
                fitness_score = 0.75 * fitness_score
                
        #check strengths
        for i in range(len(tower)):
            if (len(tower) - i - 1) > tower[i].strength:
                for j in range((len(tower) - i - 1) - tower[i].strength):
                    fitness_score = 0.75 * fitness_score

        return fitness_score

    def randomSelection(self, population, fitnessFn):
        # List of child, fitness pairs
        pop_fitnesses = [[child, fitnessFn(child)] for child in population]

        # TODO: maybe put this into the fitnessFn

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
        # print len(parent_x)
        split = random.randint(1, len(parent_x) - 1)

        # generate the sub-lists from the split
        x_left = list(parent_x[0:split])
        x_right = list(parent_x[split:])
        y_left = list(parent_y[0:split])
        y_right = list(parent_y[split:])

        # merge the sub-lists to create children
        child_a = x_left + y_right
        child_b = y_left + x_right

        better_childa = self.checkTower(child_a)
        better_childb = self.checkTower(child_b)

        return better_childa

    def mutate(self, child):
        flipOne = random.randint(0,len(child)-1)
        flipTwo = random.randint(0,len(child)-1)
        while child[flipOne] == child[flipTwo]:
            flipTwo = random.randint(0,len(child)-1)
        child[flipOne], child[flipTwo] = child[flipTwo], child[flipOne]

        return child

    def str_phenotype(self, child):
            return self.filter_traits(child)