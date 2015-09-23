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
        
        pass

    def randomSelection(self, population, fitnessFn):
        pass

    def reproduce(self, parent_x, parent_y):
        pass

    def mutate(self, child):
        pass

    def str_phenotype(self, child):
            return self.filter_traits(child)