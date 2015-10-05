import random
import time
import sys

def makeMap(rows, cols, numBats, numBombs):

    global startingCol
    global startingRow

    # Randomly pick a starting location for the robot
    startingCol = randint(0, cols - 1)
    startingRow = randint(0, rows - 1)
    
    world_map = [] #List to hold all of the world map pieces

    # Bombs cannot be placed in squares bordering the starting location

    #DFS to add all non walled neighbors to list then do the same for their neighbors
    # If not on list- regenerate map

    
    return world_map


class WorldPiece:
    def __init__(self, adjBombs, adjBats, bomb, battery):
        self.adjBombs = adjBombs
        self.adjBats = adjBats
        self.bomb = bomb 
        self.battery = battery # 0 if no battery, integer for amount of charge

    def removeBattery(self):
        self.battery = false

    def removeAdjBat(self):
        self.adjBats = self.adjBats - 1

    def addAdjBat(self):
        self.adjbats = self.adjBats + 1

    def addAdjBomb(self):
        self.adjBombs = self.adjBombs + 1

    def placeBomb(self):
        self.bomb = True

    def placeBat(self):
        self.battery = True

    def __str__(self):
        return "%d, %d, %d, %d" % (self.adjBombs, self.adjBats, self.bomb, self.battery)

class RobotPiece:
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


def main():
    # Command line format: minesweeper.py puzzleHeight puzzleWidth bumbBatteries numBombs
    puzzleHeight = int(sys.argv[1])
    puzzleWidth = int(sys.argv[2])
    numBatteries = int(sys.argv[3)
    numBombs = int(sys.argv[4])
    worldMap = makeInput(puzzleHeight, puzzleWidth, numBatteries, numBombs)

    
sys.argv = ['minesweeper.py', 4, 4, 10, 10]

if __name__ == "__main__":
    main()
