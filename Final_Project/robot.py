#from minesweeper import WorldSquare
from random import randint
import itertools
import time
import sys
from util import debug
from math import sqrt
from util import analysis

class RobotSquare:
    def __init__(self, location, flagged, probBomb, probBat, checked):
        self.loc = location
        self.flagged = flagged 
        self.probBomb = probBomb
        self.probBat = probBat
        self.checked = checked
        self.adjBombs = 0
        self.adjBatteries = 0
        
    def flag(self):
        self.flagged = True

    def setChecked(self):
        self.checked = True

    def changeBombProb(self, probability):
        self.probBomb = probability

    def changeBatProb(self, probability):
        self.probBat = probability

    def __str__(self):
        return "%s, %d, %d, %d" % (self.loc, self.flagged, self.adjBombs, self.adjBatteries)

    def __eq__(self, other):
        return self.loc == other.loc


# Class to hold all of the pieces of the robot map
class RobotMap:
    def __init__(self, robotLoc, rows, cols):
        # holds the robot map pieces
        self.robotSquares = [[RobotSquare([x, y],False,0.0,0.0,False) for y in range(rows)] for x in range(cols)]
        self.checkedSquares = [] # list of searched RobotSquares
        self.fringe = [self.getSquare(robotLoc)] # unsearched squares adjacent to searched squares
        self.bombStates = [[[False for y in range(rows)] for x in range(cols)]] # list of 2D arrays of booleans
        self.rows = rows
        self.cols = cols

    # Print out the current map
    def printMap(self, robotLoc):
        for y in range(self.rows):
            printRow = []
            for x in range(self.cols):
                val = "*"
                if self.robotSquares[x][y].checked:
                    val = "C"
                if self.robotSquares[x][y].flagged:
                    val = "B"
                if self.robotSquares[x][y].loc == robotLoc:
                    val = "R"
                printRow.append(val)
            print printRow

    def printBombStates(self):
        for i in range(len(self.bombStates)):
            debug("***Bomb State #" + str(i))
            for y in range(len(self.bombStates[i])):
                p = []
                for x in range(len(self.bombStates[i][0])):
                    p.append(self.bombStates[i][x][y])
                debug(p)

    def printBombProbabilities(self):
        debug("***BOMB PROBABILITIES***")
        for y in range(len(self.robotSquares)):
            p = []
            for x in range(len(self.robotSquares[0])):
                p.append(self.robotSquares[x][y].probBomb)
            debug(p)


    def getSquare(self, loc):
        return self.robotSquares[loc[0]][loc[1]]

    def getNeighbors(self, loc):
        # find all neighbors within the map
        width = len(self.robotSquares[0])
        height = len(self.robotSquares)
        delta_x = [-1, 0, 1,-1, 1,-1, 0, 1]
        delta_y = [-1,-1,-1, 0, 0, 1, 1, 1]
        neighbors = []
        for i in range(len(delta_x)):
            new_x = loc[0] + delta_x[i]
            new_y = loc[1] + delta_y[i]
            if 0 <= new_x < width and 0 <= new_y < height:
                neighbors.append(self.robotSquares[new_x][new_y])
        return neighbors

    # check whether a bombState has the correct number of bombs adjacent to each checked Square
    def isValidBombState(self, bombState):
        for square in self.checkedSquares:
            neighbors = self.getNeighbors(square.loc)
            # count how many neighbors have bombs in the bombState
            countAdjBombs = len([sqr for sqr in neighbors if bombState[sqr.loc[0]][sqr.loc[1]]])
            if countAdjBombs != square.adjBombs:
                return False
        return True

    # Updates self.bombStates to reflect gained information from addedLoc
    def updateBombStates(self, newAdjUnsearched):
        for newSquare in newAdjUnsearched:
            # Add new bombStates
            for state_i in range(len(self.bombStates)):
                newBombState = []
                for row in self.bombStates[state_i]:
                    newRow = list(row)
                    newBombState.append(newRow)
                newBombState[newSquare.loc[0]][newSquare.loc[1]] = True
                self.bombStates.append(newBombState)

        # Remove invalid current bombStates
        self.bombStates[:] = [state for state in self.bombStates if self.isValidBombState(state)]

    # Update the probBombs of each RobotSquare in the fringe based on new info gained
    # at addedLoc
    def updateProbabilities(self, world_square):
        # construct list of new adjacent unsearched squares
        newAdjUnsearched = []
        neighbors = self.getNeighbors(world_square.loc)
        for neighbor in neighbors:
            if not neighbor.checked and not neighbor.flagged and neighbor not in self.fringe:
                newAdjUnsearched.append(neighbor)

        self.updateBombStates(newAdjUnsearched)
        self.printBombStates()
        # go through bomb states and count how many times a bomb is in each fringe square
        fringeBombCounts = [0] * len(self.fringe)
        for bombState in self.bombStates:
            for sqr_i in range(len(self.fringe)):
                loc = self.fringe[sqr_i].loc
                if bombState[loc[0]][loc[1]]:
                    # bomb here in this fringe square in this bombState
                    fringeBombCounts[sqr_i] += 1
        # update probabilities accordingly
        for sqr_i in range(len(self.fringe)):
            self.fringe[sqr_i].probBomb = float(fringeBombCounts[sqr_i])/len(self.bombStates)

        # flag squares with probability of 1, and remove them from the fringe
        for row in self.robotSquares:
            for square in row:
                if square.probBomb == 1 and square in self.fringe:
                    square.flag()
                    self.fringe.remove(square)
        self.printBombProbabilities()    


class Robot:
    def __init__(self, initialBattery, location, rows, cols):
        self.battery = initialBattery
        self.loc = location # [0] is x, [1] is y (namedtuple?)
        self.isDead = False
        self.robotMap = RobotMap(location, rows, cols)
        
    def changeBattery(self, difference):
        self.battery += difference

    class SearchNode:
        def __init__(self, location, goalDist, pathCost):
            self.loc = location
            self.dist = goalDist
            self.cost = pathCost
    
    def frontierSort(self, node):
        return node.dist + node.cost
    
    def findPath(self, goal):
        # start the frontier with the neighbors of the current location
        frontier = []
        # get list of neighboring RobotSquares
        neighbors = self.robotMap.getNeighbors(self.loc)
        # get list of neighboring RobotSquares
        for neighbor in neighbors:
            # add all the explored neighbors to the frontier as SearchNodes
            if neighbor.checked or neighbor.loc == goal.loc:
                neighborDist = sqrt(pow((goal.loc[0] - neighbor.loc[0]), 2) + pow((goal.loc[1] - neighbor.loc[1]), 2))
                frontier.append(self.SearchNode(neighbor.loc, neighborDist, 1))
        
        frontier.sort(key = self.frontierSort)
        
        # while the goal hasn't been found, add the neighbors of the "best" node (A*)
        while frontier[0].dist != 0:
            node = frontier.pop(0)
            # get list of neighboring RobotSquares
            neighbors = self.robotMap.getNeighbors(node.loc)
            for neighbor in neighbors:
                # add all explored neighbors to the frontier as SearchNodes
                if neighbor.checked or neighbor.loc == goal.loc:
                    deltaX = abs(goal.loc[0] - neighbor.loc[0])
                    deltaY = abs(goal.loc[1] - neighbor.loc[1])
                    neighborDist = max(deltaX, deltaY)
                    neighborCost = node.cost + 1
                    frontier.append(self.SearchNode(neighbor.loc, neighborDist, neighborCost))
                frontier.sort(key=self.frontierSort)
            
        return frontier[0].cost
        
    def utilityFn(self, botSquare):
        # sortedFringe = sorted(self.robotMap.fringe, key=lambda BotSquare: BotSquare.probBomb)
        distance = max(abs(self.loc[0] - botSquare.loc[0]), abs(self.loc[1] - botSquare.loc[1]))
        bombProb = botSquare.probBomb;
        batProb = botSquare.probBat
        return (1.0 - bombProb) + (1.0 - float(distance)/self.battery)

    def chooseNextLocation(self):
        #self.battery = 1000

        sortedFringe = sorted(self.robotMap.fringe, key=self.utilityFn, reverse=True)
        for fringe_square in sortedFringe:
            pathCost = self.findPath(fringe_square)
            if pathCost <= self.battery:
                return fringe_square

    def move(self, world_square):
        if world_square.loc != self.loc:
            # if not initialization, calculate battery usage
            path_len = self.findPath(world_square)
            self.changeBattery(-path_len)
        self.loc = world_square.loc
        # search location
        # update RobotSquare
        if world_square.bomb or self.battery == 0:
            self.explode()
            return
        self.robotMap.getSquare(self.loc).setChecked()
        # add WorldSquare to checkedSquares
        self.robotMap.checkedSquares.append(world_square)
        # remove current location from fringe
        self.robotMap.fringe.remove(self.robotMap.getSquare(self.loc))
        # add neighbors of current location to fringe
        self.robotMap.updateProbabilities(world_square)
        neighbors = self.robotMap.getNeighbors(self.loc)
        for neighbor in neighbors:
            if not neighbor.checked and not neighbor.flagged and neighbor not in self.robotMap.fringe:
                self.robotMap.fringe.append(neighbor)
        debug("Fringe:")
        for square in self.robotMap.fringe:
            debug(square)

    def cantTouchThis(self):
        for fringe_square in self.robotMap.fringe:
            pathCost = self.findPath(fringe_square)
            if pathCost <= self.battery:
                return False
        return True
    
    def explode(self):
        self.isDead = True
