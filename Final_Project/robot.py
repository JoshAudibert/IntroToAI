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

	def move(self):
		pass

	def explode(self):
		self.isDead = True

	def

