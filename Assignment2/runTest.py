import sys
import ga

# parse the command line inputs, run A*, print the results
def main():
    ga1 = ga.parseInput(1, 'problem1_test1.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(1, 'problem1_test2.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(1, 'problem1_test3.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(2, 'problem2_test1.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(2, 'problem2_test2.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(2, 'problem2_test3.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(3, 'problem3_test1.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(3, 'problem3_test2.txt')
    ga.runGA(ga1, 10)
    ga1 = ga.parseInput(3, 'problem3_test3.txt')
    ga.runGA(ga1, 10)
    
if __name__ == "__main__":
    main()
