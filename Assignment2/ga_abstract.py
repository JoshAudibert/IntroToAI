import abc

# This is the abstract GeneticAlgorithm class that each problem implements

class GeneticAlgorithm:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generatePopulation(self):
        """Implement this per puzzle
        Return:
            A list of length self.POP_SIZE containing the original population
        """

    @abc.abstractmethod
    def fitnessFn(self, child):
        """Implement this per puzzle
        Args:
            child: a child of the population
        Return:
            A real number representing the fitness of the child. Scale can differ per GeneticAlgorithm
        """

    @abc.abstractmethod
    def randomSelection(self, population):
        """Implement this per puzzle
        Args:
            population: a list containing the current population
        Return:
            A single individual that will be a parent of the next generation
        """

    @abc.abstractmethod
    def reproduce(self, parent_x, parent_y):
        """Implement this per puzzle
        Args:
            parent_x, parent_y: the two parents that will be split to create a single child
        Return:
            The single child created
        """

    @abc.abstractmethod
    def mutate(self, child):
        """Implement this per puzzle
        Args:
            child: a child of the population
        Return:
            The mutated child
        """

    @abc.abstractmethod
    def str_phenotype(self, child):
        """Implement this per puzzle
        Args:
            child: a child of the population
        Return:
            A more readable version of the child representation
        """

    @abc.abstractmethod
    def score(self, child):
        """Implement this per puzzle
        Args:
            child: a child of the population
        Return:
            A real number representing the score of the child based on the rules given in the assignment description
        """
        
    @abc.abstractmethod
    def cull(self, population, num_cull):
        """Implement this per puzzle
        Args:
            population: the current population
            num_cull: the number of children to cull out of the population
        """
        
    @abc.abstractmethod
    def getElites(self, population, num_elite):
        """Implement this per puzzle
        Args:
            population: the current population
            num_elite: the number of parents to keep for the next generation
        Return:
            A list of the num_elite parents that will be kept for the next generation
        """
