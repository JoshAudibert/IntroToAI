import problem1, problem2, problem3
import random
import abc

# Genetic Algorithm
class GeneticAlgorithm:
	__metaclass__ = abc.ABCMeta

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

    # create GeneticAlgorithm based on puzzleNum
    if puzzleNum == 1:
    	ga = AddingGA()
    elif puzzleNum == 2:
    	ga = BinGA()
    elif puzzleNum == 3:
    	ga = TowerGA()
    else:
    	print "Please input a puzzle number between 1 and 3 inclusive"
    	exit()

    f = open(inputfile, 'r')

    # Parse file according to problem


    return geneticAlgorithm



def runGA():
	population = []
	# set up population
	fitnessFn
	time = 0
	timeAllowed
	mutation_prob = .001
	done = False
	while not done:
		new_population = []
		for in range(len(population)):
			parent_x = randomSelection(population, fitnessFn)
			# potentially temporarily remove parent_x from population so parent_y isn't also parent_x
			parent_y = randomSelection(population, fitnessFn)
			child = reproduce(parent_x, parent_y)
			if random.random() <= mutation_prob:
				child = mutate(child)
			new_population.append(child)
		population = new_population
		if time >= timeAllowed:
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
