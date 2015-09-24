import sys
import ga

# parse the command line inputs, run A*, print the results
def main():
    print "Problem 1 Test 1:"
    ga1 = ga.parseInput(1, 'problem1_test1.txt')
    ga.runGA(ga1, 10, 'prob1_test1_results.csv')
    print "Problem 1 Test 2:"
    ga1 = ga.parseInput(1, 'problem1_test2.txt',)
    ga.runGA(ga1, 10, 'prob1_test2_results.csv')
    print "Problem 1 Test 3:"
    ga1 = ga.parseInput(1, 'problem1_test3.txt')
    ga.runGA(ga1, 10, 'prob1_test3_results.csv')
    print "Problem 2 Test 1:"
    ga1 = ga.parseInput(2, 'problem2_test1.txt')
    ga.runGA(ga1, 10, 'prob2_test1_results.csv')
    print "Problem 2 Test 2:"
    ga1 = ga.parseInput(2, 'problem2_test2.txt')
    ga.runGA(ga1, 10, 'prob2_test2_results.csv')
    print "Problem 2 Test 3:"
    ga1 = ga.parseInput(2, 'problem2_test3.txt')
    ga.runGA(ga1, 10, 'prob2_test3_results.csv')
    print "Problem 3 Test 1:"
    ga1 = ga.parseInput(3, 'problem3_test1.txt')
    ga.runGA(ga1, 10, 'prob3_test1_results.csv')
    print "Problem 3 Test 2:"
    ga1 = ga.parseInput(3, 'problem3_test2.txt')
    ga.runGA(ga1, 10, 'prob3_test2_results.csv')
    print "Problem 3 Test 3:"
    ga1 = ga.parseInput(3, 'problem3_test3.txt')
    ga.runGA(ga1, 10, 'prob3_test3_results.csv')
    
if __name__ == "__main__":
    main()
