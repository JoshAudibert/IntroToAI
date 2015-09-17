import problem1, problem2, problem3
import random

# Genetic Algorithm

# parse the input differently depending on which problem is being run
def parseInput(inputfile, problemNum):
    f = open(inputfile, 'r')

def mutate(child):
	pass


def reproduce(parent_x, parent_y):
	pass


def randomSelection(population, fitnessFn):
	pass


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
    parseInput(filename, puzzleNum)

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
   
    runGA(ga)
    
    
if __name__ == "__main__":
    main()
