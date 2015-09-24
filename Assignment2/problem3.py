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

    def __str__(self):
        return "%s, %d, %d, %d" % (self.pieceType, self.width, self.strength, self.cost)

class TowerGA(GeneticAlgorithm):
    def __init__(self, pieces):
        # initialize population
        self.POP_SIZE = 20
        self.pieces = list(pieces)

    # Determine if there are two pieces at the same level
    # or if the tower is missing a level
    def checkTower(self, child):
        checkList = [0] * (len(self.pieces) + 1)
        for i in range(len(child)):
            if child[i]:
                if checkList[child[i]]:
                    child[i] = 0
                else:
                    checkList[child[i]] = 1
        return child

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
    
    def fitnessFn(self, child):
        if child.count(0) == len(child):
            return 0

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
        filtered = []
        for i in range(len(child)):
            if child[i]:
                filtered.append(str(self.pieces[i]))
        return filtered


    def randomSelection(self, population, fitnessFn):
        # List of child, fitness pairs
        pop_fitnesses = [[child, fitnessFn(child)] for child in population]
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

        better_child_a = self.checkTower(child_a)
        better_child_b = self.checkTower(child_b)

        return better_child_a

    #
    def mutate(self, child):
        non_zero_indices = []
        for i in range(len(child)):
            if child[i]:
                non_zero_indices.append(i)

        # if all zeros or only one piece
        if len(non_zero_indices) <= 1:
            child[random.randint(0, len(child)-1)] = random.randint(1, len(self.pieces))
            return child

        flipOne = random.randint(0, len(non_zero_indices)-1)
        childCopy = list(child)
        del childCopy[flipOne]
        flipTwo = random.randint(0, len(childCopy)-1)
        print childCopy, child, child[flipOne], child[flipTwo]

        # switch pieces
        child[flipOne], child[flipTwo] = child[flipTwo], child[flipOne]
        #child = self.checkTower(child)
        return child


    def str_phenotype(self, child):
            return self.filter_traits(child)


    def countBrokenRules(self, child):
        num_broken_rules = 0

        # build tower
        tower = [0] * len(self.pieces)
        for i in range(len(child)):
            if child[i]:
                try:
                    tower[child[i]-1] = self.pieces[i]
                except:
                    import ipdb; ipdb.set_trace()
                    print "HERE"
        
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
                # for j in range((len(tower)-1 - i) - tower[i].strength):
                #     fitness_score = 0.75 * fitness_score
        return num_broken_rules
        
    def cull(self, population, num_cull):
        sorted_pop = sorted(population, key = self.fitnessFn)
        for i in range(num_cull):
            population.remove(sorted_pop[i])
            
    def getElites(self, population, num_elite):
        sorted_pop = sorted(population, key = self.fitnessFn)
        elites = []
        for i in range(num_elite):
            elites.append(sorted_pop[len(sorted_pop) - 1 - i])
        return elites

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
