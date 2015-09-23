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
        ga = AddingGA(11, [2,3,5,7])
    elif puzzleNum == 2:
        lines = f.read().splitlines()
        int_list = [int(i) for i in lines]
        # Add list to new genetic algorithm
        ga = BinGA(lint_list)
    elif puzzleNum == 3:
        # Read in all numbers from the file
        lines = f.read().splitlines()
        pieces = list()

        for count in xrange(len(lines)):
            nums = lines[count].split()
            pieceType = nums[0].replace(',', '')
            width = int(nums[1].replace(',', ''))
            strength = int(nums[2].replace(',', ''))
            cost = int(nums[3].replace(',', ''))
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

    # set initial variables
    timeAllowed = 2
    mutation_prob = .001
    done = False
    numGens = 1
    start_time = time.time()

    while not done:
        new_population = []
        numGens += 1
        for x in range(len(population)):
            parent_x = ga.randomSelection(population, ga.fitnessFn)
            # TODO: potentially temporarily remove parent_x from population so parent_y isn't also parent_x
            parent_y = ga.randomSelection(population, ga.fitnessFn)
            child = ga.reproduce(parent_x, parent_y)
            if random.random() <= mutation_prob:
				child = ga.mutate(child)

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
    print ga.str_phenotype(population[fit_index])
    print "Number of generations: " + str(numGens)


# parse the command line inputs, run the genetic algorithm, print the results
def main():
    # Command line format: ga.py puzzle# filename timeLimit
    puzzleNum = int(sys.argv[1])
    filename = sys.argv[2]
    timeLimit = sys.argv[3]
    ga = parseInput(puzzleNum, filename, timeLimit)
    runGA(ga)
    

sys.argv = ['ga.py', 1, 'problem1_test1.txt', 1000]
if __name__ == "__main__":
    main()
