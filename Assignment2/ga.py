from problem1 import AddingGA
from problem2 import BinGA
from problem3 import TowerGA
from ga_abstract import GeneticAlgorithm
import random
import time
import abc
import sys

# parse the input differently depending on which problem is being run
def parseInput(puzzleNum, inputfile, timeLimit):

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
	population = ga.generatePopulation()
	# set up population
	# fitnessFn
	# time = 0
	timeAllowed = 10
	mutation_prob = .001
	done = False
	start_time = time.time()
	while not done:
		new_population = []
		for x in range(len(population)):
			parent_x = ga.randomSelection(population, ga.fitnessFn)
			# potentially temporarily remove parent_x from population so parent_y isn't also parent_x
			parent_y = ga.randomSelection(population, ga.fitnessFn)
			child = ga.reproduce(parent_x, parent_y)
			#if random.random() <= mutation_prob:
			#	child = ga.mutate(child)
			new_population.append(child)
		population = new_population
		if time.time() - start_time >= timeAllowed:
			done = True
	
	print "best solution"
	best_fit = ga.fitnessFn(population[0])
	fit_index = 0
	for individual in population:
		if(ga.fitnessFn(individual) < best_fit):
			best_fit = ga.fitnessFn(individual)
			fit_index = population.index(individual)
	print population[fit_index]
#sys.argv = ['ga.py', 1, 'Test1.txt', 1000]

# parse the command line inputs, run the genetic algorithm, print the results
def main():
    # Command line format: ga.py puzzle# filename timeLimit
    puzzleNum = int(sys.argv[1])
    filename = sys.argv[2]
    timeLimit = sys.argv[3]
    ga = parseInput(puzzleNum, filename, timeLimit)

    
   
    runGA(ga)
    
    
if __name__ == "__main__":
    main()
