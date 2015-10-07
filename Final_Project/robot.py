from random import randint
import time
import sys

class RobotSquare:
    def __init__(self, flagged, battery, probBomb, probBat, checked):
        self.flagged = flagged 
        self.probBomb = probBomb
        self.probBat = probBat
        self.checked = checked
        
    def flag(self):
        self.flagged = True

    def setChecked(self):
        self.checked = True

    def changeBombProb(self, probability):
        self.probBomb = probability

    def changeBatProb(self, probability):
        self.probBat = probability

    def setChecked(self):
        self.checked = True

    def __str__(self):
        return "%d, %d, %d, %d" % (self.bomb, self.battery)

class Robot:
	def __init__(self, initialBattery, roomWidth, roomHeight, location):
		self.battery = initialBattery
		self.loc = location # [0] is x, [1] is y (namedtuple?)
		self.isDead = False
		#self.isOnPath = False # true when Robot has set path it's on
		#self.path = [] # When isOnPath, ordered list of 'N', 'S', 'E', and 'W'
		self.currentMap = []
		# initialize map
		for row in range(roomWidth):
			mapRow = []
			for col in range(roomHeight):
				mapRow.append(RobotSquare(False, 0, 0, 0, False))
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

	def updateProbabilities(self, addedLoc):
		# construct list of new adjacent unsearched squares
		newAdjUnsearched = self.getNeighbors(addedLoc)

		# For each hypothesis state (either WorldMap or 2D array of booleans)
		for bombState in bombStates:



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


