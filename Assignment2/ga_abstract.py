import abc

# Genetic Algorithm
class GeneticAlgorithm:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generatePopulation(self):
        """Implement this per puzzle"""

    @abc.abstractmethod
    def fitnessFn(self, child):
        """Implement this per puzzle"""

    @abc.abstractmethod
    def randomSelection(self, population, fitnessFn):
        """Implement this per puzzle"""

    @abc.abstractmethod
    def reproduce(self, parent_x, parent_y):
        """Implement this per puzzle"""

    @abc.abstractmethod
    def mutate(self, child):
        """Implement this per puzzle"""
