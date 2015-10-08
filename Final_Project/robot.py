from random import randint
import time
import sys

class RobotSquare:
    def __init__(self, location, flagged, battery, probBomb, probBat, checked):
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

<<<<<<< HEAD
# Class to hold all of the pieces of the robot map
class RobotMap:
    def __init__(self, robotSquares):
        self. robotSquares = robotSquares # holds the robot map pieces
        self.checkedSquares = [] # list of searched RobotSquares
	self.fringe = [] # unsearched squares adjacent to searched squares
	self.bombStates = [] # list of 2D arrays of booleans

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
	def __init__(self, initialBattery, roomWidth, roomHeight, location):
		self.battery = initialBattery
		self.loc = location # [0] is x, [1] is y (namedtuple?)
		self.isDead = False
		#self.bombStates = [] # list of 2D arrays of booleans
		#self.isOnPath = False # true when Robot has set path it's on
		#self.path = [] # When isOnPath, ordered list of 'N', 'S', 'E', and 'W'
		#self.checkedSquares = [] # list of searched RobotSquares
		#self.fringe = [] # unsearched squares adjacent to searched squares
		self.currentMap = []
		# initialize map
		for row in range(roomWidth):
			mapRow = []
			for col in range(roomHeight):
				mapRow.append(RobotSquare([col, row], False, 0, 0, 0, False))
			self.currentMap.append(mapRow)
		# set initial loca


	def changeBattery(self, difference):
		self.battery += difference

	def move(self):
		# we have current list of hypotheses (valid bomb states)
		# and thus have bomb probabilities of fringe squares
		#if isOnPath:

		# based on probability map, choose best location to search
		# TELEPORT!!
		# search location
		# update probabilities
		# update battery if you feel like it
		# update fringe

	def explode(self):
		self.isDead = True
=======

class Robot:
    def __init__(self, initialBattery, roomWidth, roomHeight, location):
        self.battery = initialBattery
        self.loc = location # [0] is x, [1] is y (namedtuple?)
        self.isDead = False
        self.bombStates = [] # list of 2D arrays of booleans
        #self.isOnPath = False # true when Robot has set path it's on
        #self.path = [] # When isOnPath, ordered list of 'N', 'S', 'E', and 'W'
        self.checkedSquares = [] # list of searched RobotSquares
        self.fringe = [] # unsearched squares adjacent to searched squares
        self.currentMap = []
        # initialize map
        for row in range(roomWidth):
            mapRow = []
            for col in range(roomHeight):
                mapRow.append(RobotSquare([col, row], False, 0, 0, 0, False))
            self.currentMap.append(mapRow)
        # set initial loca


    def changeBattery(self, difference):
        self.battery += difference


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


    def move(self):
        # we have current list of hypotheses (valid bomb states)
        # and thus have bomb probabilities of fringe squares
        #if isOnPath:

        # based on probability map, choose best location to search
        # TELEPORT!!
        # search location
        # update probabilities
        # update battery if you feel like it

    def explode(self):
        self.isDead = True
>>>>>>> origin/master


