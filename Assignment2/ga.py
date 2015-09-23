from problem1 import AddingGA
from problem2 import BinGA
from problem3 import TowerGA
from problem3 import towerPiece
import random
import time
import sys

# parse the input differently depending on which problem is being run
def parseInput(puzzleNum, inputfile, timeLimit):

    f = open(inputfile, 'r')

    # create GeneticAlgorithm based on puzzleNum
    if puzzleNum == 1:

        lines = f.read().splitlines()
        int_list = [int(i) for i in lines]
        # First number is the target number
        targetNum = int(int_list.pop(0))
        # Add list and target number to new genetic algorithm
        ga = AddingGA(targetNum, int_list)

    elif puzzleNum == 2:
        lines = f.read().splitlines()
        float_list = [float(i) for i in lines]
        # Add list to new genetic algorithm
        ga = BinGA(float_list)

        print float_list
        
    elif puzzleNum == 3:
        # Read in all numbers from the file
        lines = f.read().splitlines()
        pieces = list()

        for line in lines:
            nums = line.split(', ')
            pieceType = nums[0]
            width = int(nums[1])
            strength = int(nums[2])
            cost = int(nums[3])
            currPiece = towerPiece(pieceType, width, strength, cost)
            pieces.append(currPiece)

        ga = TowerGA(pieces)

    else:
        print "Please input a puzzle number between 1 and 3 inclusive"
        exit()

    return ga

def runGA(ga):
    # set up initial population
    population = ga.generatePopulation()
    
    #for i in range(len(population)):
    #   print population[i]

    # set initial variables
    timeAllowed = 4
    mutation_prob = .05
    done = False
    numGens = 1
    start_time = time.time()
    best_individual = population[0]
    best_score = ga.score(best_individual)
    best_gen = 1

    while not done:
    	# look for new best fitness
    	for individual in population:
	        if(ga.score(individual) > best_score):
	            best_score = ga.score(individual)
	            best_individual = individual
	            best_gen = numGens
        new_population = []
        numGens += 1
        for x in range(len(population)):
            parent_x = ga.randomSelection(population, ga.fitnessFn)
            # TODO: potentially temporarily remove parent_x from population so parent_y isn't also parent_x
            parent_y = ga.randomSelection(population, ga.fitnessFn)
            print parent_x, parent_y, numGens
            child = ga.reproduce(parent_x, parent_y)
            if random.random() <= mutation_prob:
                child = ga.mutate(child)
            new_population.append(child)
        population = new_population
        if time.time() >= timeAllowed + start_time:
        	done = True

    print "*** Best solution"
    print "Individual: ", ga.str_phenotype(best_individual)
    #print "Num Broken rules: ", ga.countBrokenRules(best_individual)
    print "Score: ", best_score
    #print "Fitness: ", ga.fitnessFn(best_individual)
    print "Generation found: ", best_gen
    print "Number of generations: " + str(numGens)


# parse the command line inputs, run the genetic algorithm, print the results
def main():
    # Command line format: ga.py puzzle# filename timeLimit
    puzzleNum = int(sys.argv[1])
    filename = sys.argv[2]
    timeLimit = sys.argv[3]
    ga = parseInput(puzzleNum, filename, timeLimit)
    runGA(ga)
    
sys.argv = ['ga.py', 3, 'problem3_test1.txt', 1000]

if __name__ == "__main__":
    main()
