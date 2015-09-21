from problem1 import AddingGA
from problem2 import BinGA
from problem3 import TowerGA
import random
import time
import abc

# Genetic Algorithm
class GeneticAlgorithm:
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod
	def generatePopulaiton(self):
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

# parse the input differently depending on which problem is being run
def parseInput(problemNum, inputfile, timeLimit):

    f = open(inputfile, 'r')
	
    # create GeneticAlgorithm based on puzzleNum
    if puzzleNum == 1:
    	ga = AddingGA(11, [2,3,5,7])
    elif puzzleNum == 2:
    	ga = BinGA()
    elif puzzleNum == 3:
    	ga = TowerGA()
    else:
    	print "Please input a puzzle number between 1 and 3 inclusive"
    	exit()

    # Parse file according to problem


    return ga



def runGA(ga):
	population = ga.generatePopulaiton
	# set up population
	# fitnessFn
	time = 0
	timeAllowed = 10
	mutation_prob = .001
	done = False
	start_time = time.time()
	while not done:
		new_population = []
		for x in range(len(population)):
			parent_x = randomSelection(population, fitnessFn)
			# potentially temporarily remove parent_x from population so parent_y isn't also parent_x
			parent_y = randomSelection(population, fitnessFn)
			child = reproduce(parent_x, parent_y)
			if random.random() <= mutation_prob:
				child = mutate(child)
			new_population.append(child)
		population = new_population
		if time.time() - start_time >= timeAllowed:
			done = True

sys.argv = ['ga.py', 1, 'Test1.txt', 1000]

# parse the command line inputs, run the genetic algorithm, print the results
def main():
    # Command line format: ga.py puzzle# filename timeLimit
    puzzleNum = sys.argv[1]
    filename = sys.argv[2]
    timeLimit = sys.argv[3]
    ga = parseInput(filename, puzzleNum)

    
   
    runGA(ga)
    
    
if __name__ == "__main__":
    main()
