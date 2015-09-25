from problem1 import AddingGA
from problem2 import BinGA
from problem3 import TowerGA
from problem3 import towerPiece
import random
import time
import sys
import csv

# parse the input differently depending on which problem is being run
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
        print lines
        float_list = [float(i) for i in lines]
        # Add list to new genetic algorithm
        ga = BinGA(float_list)

        print float_list
        
    elif puzzleNum == 3:
        # Read in all numbers from the file
        lines = f.read().splitlines()
        pieces = list()

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


def runGA(ga, timeLimit, resultsFile):
    testing = True
    if testing:
        data = {}

    # set up initial population
    population = ga.generatePopulation()

    # set initial variables
    timeAllowed = timeLimit
    mutation_prob = .05
    done = False
    numGens = 1
    num_cull = 0
    num_elite = 0
    print_gens = 50
    start_time = time.time()
    best_individual = population[0]
    best_score = ga.score(best_individual)
    best_gen = 1

    with open(resultsFile, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        while not done:
            # look for new best fitness
            for individual in population:
                if(ga.score(individual) > best_score):
                    best_score = ga.score(individual)
                    best_individual = individual
                    best_gen = numGens
            new_population = []
            if numGens % print_gens == 1:
                sorted_pop = sorted(population, key = ga.score, reverse = True)
                gen_best = ga.score(sorted_pop[0])
                gen_median = ga.score(sorted_pop[len(sorted_pop)//2]) if len(sorted_pop) % 2 == 1 else (ga.score(sorted_pop[(len(sorted_pop)+1)//2]) + ga.score(sorted_pop[(len(sorted_pop)-1)//2]))/2.0
                gen_worst = ga.score(sorted_pop[-1])
                    
                if testing:
                    data[numGens] = [gen_best, gen_worst, gen_median]
                else:
                    print "Generation Data:"
                    print "number: ", numGens
                    print "best individual score: ", gen_best
                    print "median individual score: ", gen_median
                    print "worst individual score: ", gen_worst
                    csvwriter.writerow([numGens, gen_best, gen_median, gen_worst])
                
            numGens += 1
            for x in range(len(population) + num_cull - num_elite):
                parent_x = ga.randomSelection(population, ga.fitnessFn)
                # TODO: potentially temporarily remove parent_x from population so parent_y isn't also parent_x
                parent_y = ga.randomSelection(population, ga.fitnessFn)
                child = ga.reproduce(parent_x, parent_y)
                if random.random() <= mutation_prob:
                    child = ga.mutate(child)
                new_population.append(child)
           
            if num_elite > 0:
                new_population.extend(ga.getElites(population, num_elite))
          
            if num_cull > 0:
                ga.cull(new_population, num_cull)
            
            population = new_population
            if time.time() >= timeAllowed + start_time:
                done = True

        print "*** Best solution"
        print best_individual
        print "Individual: ", ga.str_phenotype(best_individual)
        #print "Num Broken rules: ", ga.countBrokenRules(best_individual)
        print "Score: ", best_score
        #print "Fitness: ", ga.fitnessFn(best_individual)
        print "Generation found: ", best_gen
        print "Number of generations: " + str(numGens)
        print ga.score(best_individual)
    if testing:
        return data


# parse the command line inputs, run the genetic algorithm, print the results
def main():
    testing = True
    # Command line format: ga.py puzzle# filename timeLimit
    if not testing:
        puzzleNum = int(sys.argv[1])
        filename = sys.argv[2]
        timeLimit = sys.argv[3]
        ga = parseInput(puzzleNum, filename)
        runGA(ga, timeLimit, 'resultsFile.csv')
    else:
        # testing
        # run each of the problems for test 3 five times and average them per generation
        prob1_data = []
        prob2_data = []
        prob3_data = []
        # Start with problem 1:
        for i in range(5):
            ga = parseInput(1, 'problem1_test4.txt')
            # data is a dict mapping genNum to a list of [best, worst, median]
            data = runGA(ga, 0, 'resultsFile.csv')
            prob1_data.append(data)

        # problem 2:
        for i in range(5):
            ga = parseInput(2, 'problem2_test4.txt')
            # data is a dict mapping genNum to a list of [best, worst, median]
            data = runGA(ga, 0, 'resultsFile.csv')
            prob2_data.append(data)

        # problem 3:
        for i in range(5):
            ga = parseInput(3, 'problem3_test2.txt')
            # data is a dict mapping genNum to a list of [best, worst, median]
            data = runGA(ga, 10, 'resultsFile.csv')
            prob3_data.append(data)

        def writeProblem(prob_data, file):
            with open(file, 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                gen = 1
                minGen = max(prob1_data[0].keys())
                for data in prob_data:
                    if max(data.keys()) < minGen:
                        minGen = max(data.keys())
                minGen = minGen - (minGen % 50) + 1
                while gen <= minGen:
                    csvwriter.writerow([gen, sum([data[gen][0] for data in prob_data])/5.0,
                                        sum([data[gen][1] for data in prob_data])/5.0,
                                        sum([data[gen][2] for data in prob_data])/5.0])
                    gen += 50

        # average the results and print them to the resultsFile.csv
        writeProblem(prob1_data, 'resultsFile1.csv')
        writeProblem(prob2_data, 'resultsFile2.csv')
        writeProblem(prob3_data, 'resultsFile3.csv')

    
sys.argv = ['ga.py', 3, 'problem3_test3.txt', 20]

if __name__ == "__main__":
    main()
