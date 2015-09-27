from problem1 import AddingGA
from problem2 import BinGA
from problem3 import TowerGA, towerPiece
import random
import time
import sys

# Parse the input differently depending on which problem is being run
def parseInput(puzzleNum, inputfile):
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
    elif puzzleNum == 3:
        # Read in all numbers from the file
        lines = f.read().splitlines()
        pieces = []
        for line in lines:
            nums = line.split()
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


# Runs the input GeneticAlgorithm for timeLimit seconds 
def runGA(ga, timeLimit):
    # set up initial population
    population = ga.generatePopulation()

    # set initial variables
    timeLimit
    done = False
    numGens = 1
    num_cull = 0
    num_elite = 0
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
        # generate POP_SIZE + num cull - num elite new children for the next generation
        for x in range(ga.POP_SIZE + num_cull - num_elite):
            # Select parents
            parent_x = ga.randomSelection(population)
            parent_y = ga.randomSelection(population)
            # create child
            child = ga.reproduce(parent_x, parent_y)
            # mutate with probability MUTATION_PROB
            if random.random() <= ga.MUTATION_PROB:
                child = ga.mutate(child)
            # add child to the new population
            new_population.append(child)
       
        # add the elite from the previous generation to the new population
        if num_elite > 0:
            new_population.extend(ga.getElites(population, num_elite))
      
        # cull the lowest scoring children from the new population
        if num_cull > 0:
            ga.cull(new_population, num_cull)
        
        population = new_population
        # check if timeLimit has been reached
        if time.time() >= timeLimit + start_time:
            done = True

    # output final results
    print "*** Best solution ***"
    print "Individual: ", ga.str_phenotype(best_individual)
    print "Score: ", best_score
    print "Generation found: ", best_gen
    print "Number of generations: " + str(numGens)


# parse the command line inputs and run the genetic algorithm
def main():
    # Command line format: ga.py puzzle# filename timeLimit
    puzzleNum = int(sys.argv[1])
    filename = sys.argv[2]
    timeLimit = sys.argv[3]
    ga = parseInput(puzzleNum, filename)
    runGA(ga, timeLimit)

    
#sys.argv = ['ga.py', 3, 'problem3_test4.txt', 10]

if __name__ == "__main__":
    main()
