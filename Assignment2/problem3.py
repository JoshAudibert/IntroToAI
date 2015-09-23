from ga_abstract import GeneticAlgorithm

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

