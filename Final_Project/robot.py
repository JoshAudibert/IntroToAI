from minesweeper import WorldSquare
from random import randint
import time
import sys

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
        return "%d, %d, %d, %d" % (self.bomb, self.battery)

# Class to hold all of the pieces of the robot map
class RobotMap:
    def __init__(self, robotSquares, width, height):
        self. robotSquares = robotSquares # holds the robot map pieces
        self.checkedSquares = [] # list of searched RobotSquares
        self.fringe = [] # unsearched squares adjacent to searched squares
        self.bombStates = [] # list of 2D arrays of booleans
        self.width = width
        self.height = height

    def getNeighbors(self, loc):
        # find all neighbors within the map
        width = len(self.currentMap[0])
        height = len(self.currentMap)
        delta_x = [-1, 0, 1,-1, 1,-1, 0, 1]
        delta_y = [-1,-1,-1, 0, 0, 1, 1, 1]
        neighbors = []
        for i in range(len(delta_x)):
            new_x = loc[0] + delta_x
            new_y = loc[1] + delta_y
            if 0 <= new_x < width and 0 <= new_y < height:
                neighbors.append(self.currentMap[new_x][new_y])
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
    def updateBombStates(self, addedLoc):
        # construct list of new adjacent unsearched squares
        newAdjUnsearched = []
        neighbors = self.getNeighbors(addedLoc)
        for neighbor in neighbors:
            if not neighbor.checked and neighbor not in self.fringe:
                newAdjUnsearched.append(neighbor)

        for newSquare in newAdjUnsearched:
            # Add new bombStates
            for bombState in self.bombStates:
                newBombState = list(bombState)
                newBombState[newSquare.loc[0]][newSquare.loc[1]] = True
                self.bombStates.append(newBombState)

        # Remove invalid current bombStates
        self.bombStates[:] = [state for state in self.bombStates if self.isValidBombState(state)]


    # Update the probBombs of each RobotSquare in the fringe based on new info gained
    # at addedLoc
    def updateProbabilities(self, addedLoc):
        self.updateBombStates(addedLoc)
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

class Robot:
    def __init__(self, initialBattery, location, robotMap):
        self.battery = initialBattery
        self.loc = location # [0] is x, [1] is y (namedtuple?)
        self.isDead = False
        self.robotMap = robotMap
        
        '''# initialize map using world map
        for row in range(self.robotMap.width):
            mapRow = []
            for col in range(self.robotMap.height):
                mapRow.append(RobotSquare([col, row], False, 0, 0, 0, False))
            self.currentMap.append(mapRow)
        # set initial loca'''



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
        neighbors = self.currentMap.getNeighbors(self.loc)
        # get list of neighboring RobotSquares
        for i in range(len(neighbors)):
            # add all the explored neighbors to the frontier as SearchNodes
            if(neighbors[i].checked):
                neighborLoc = neighbor[i].loc
                neighborDist = sqrt(pow((goal[0] - neighborLoc[0]), 2) + pow((goal[1] - neighborLoc[1]), 2))
                frontier.append(SearchNode(neighborLoc, neighborDist, 1))
        
        frontier.sort(key = frontierSort)
        
        # while the goal hasn't been found, add the neighbors of the "best" node (A*)
        while(frontier[0].dist != 0):
            node = frontier.pop(0)
            # get list of neighboring RobotSquares
            neighbors = self.currentMap.getNeighbors(node.loc)
            # add all explored neighbors to the frontier as SearchNodes
            if(neighbors[i].checked):
                neighborLoc = neighbor[i].loc
                neighborDist = sqrt(pow((goal[0] - neighborLoc[0]), 2) + pow((goal[1] - neighborLoc[1]), 2))
                neighborCost = neighbors[i].cost + 1
                frontier.append(SearchNode(neighborLoc, neighborDist, neigborCost))
            frontier.sort(key = frontierSort)
            
        return frontier[0].cost
    

    def chooseNextLocation(self):
        # sort fringe by probability of bomb
        sortedFringe = sorted(self.currentMap.fringe, key = lambda BotSquare: BotSquare.probBomb)
        return sortedFringe[0]


    def move(self):
	# we have current list of hypotheses (valid bomb states)
	# and thus have bomb probabilities of fringe squares

	# based on probability map, choose best location to search
	# TELEPORT!!
	# search location
	# update probabilities
    	# update battery
	# update fringe
        
        battery = False
        
        if(battery):
            # assume utility function scoring fringe squares according to bomb probability and distance from current location
            sortedFringe = sorted(self.currentMap.fringe, key = utilityFn)
            destinationPicked = False
            for i in range(len(sortedFringe)):
                pathCost = findPath(sortedFringe[i])
                if(pathCost < self.battery):
                    # fringe is a list of RobotSquares?
                    self.loc = sortedFringe[i].loc
                    self.battery -= pathCost
                    # TODO: search location
                    # assuming newLoc is the world square of the new location
                    # add current location to checked squares, should probably also check for dying
                    self.currentMap.checkedSquares.append(RobotSquare(self.loc, False, 0, newLoc.bomb, 0, True))
                    # remove current location from fringe, don't think below will work, find elegant way...
                    # self.currentMap.fringe.remove(self.loc)
                    # add neighbors of current location to fringe
                    self.currentMap.fringe.extend(self.currentMap.getNeighbors(self.loc))
                    self.currentMap.updateProbabilities(self.loc)
                    destinationPicked = True
                    
            if destinationPicked == False:
                # could not find a fringe square we can get to, should end run somehow
                pass
        else:
            #sort fringe by probability of bomb
            sortedFringe = sorted(self.currentMap.fringe, key = lambda BotSquare: BotSquare.probBomb)
            self.loc = sortedFringe[i].loc
            # search location
            self.currentMap.checkedSquares.append(WorldSquare(self.loc, ))
            # assuming newLoc is the world square of the new location
            # add current location to checked squares, should probably also check for dying
            self.currentMap.checkedSquares.append(RobotSquare(self.loc, False, 0, newLoc.bomb, 0, True))
            # remove current location from fringe, don't think below will work, find elegant way...
            # self.currentMap.fringe.remove(self.loc)
            # add neighbors of current location to fringe
            self.currentMap.fringe.extend(self.currentMap.getNeighbors(self.loc))
            self.currentMap.updateProbabilities(self.loc)
            destinationPicked = True

	def explode(self):
		self.isDead = True
