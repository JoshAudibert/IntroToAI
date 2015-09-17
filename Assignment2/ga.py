import random

# Genetic Algorithm



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


# parse the command line inputs, run the genetic algorithm, print the results
def main():
    runGA()
    
if __name__ == "__main__":
    main()