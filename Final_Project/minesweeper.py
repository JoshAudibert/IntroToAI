from random import randint
import time
import sys

def makeMap(rows, cols, numBats, numBombs):

    global startingCol
    global startingRow
    world_map = []

    # Neighboring Corrdinates
    numNeighbors = 8
    # (-1,-1) (0,-1) (1,-1)
    # (-1, 0) robot  (1, 0)
    # (-1, 1) (0, 1) (1, 1)
    adj_x = [-1,0,1,-1,1,-1,0,1]
    adj_y = [-1,-1,-1,0,0,1,1,1]

    # Randomly pick a starting location for the robot
    startingCol = randint(0, cols - 1)
    startingRow = randint(0, rows - 1)
    print "startingCol: ", startingCol
    print "startingRow: ", startingRow

    #List to hold all of the world map pieces
    for j in range(cols):
        col = []
        for k in range(rows):
            col.append(WorldSquare(0,0,0,0))
        world_map.append(col)

    # Place numBombs number of bombs randomly
    for i in range(numBombs):
        bomb_x = randint(0, cols - 1)
        bomb_y = randint(0, rows - 1)       

        # Bombs cannot be placed in squares bordering the starting location
        while (abs(startingCol - bomb_x) <= 1 and abs(startingRow - bomb_y) <= 1) or world_map[bomb_x][bomb_y].bomb:
            bomb_x = randint(0, cols - 1)
            bomb_y = randint(0, rows - 1)

        world_map[bomb_x][bomb_y].placeBomb() # Add bomb
        print "Bomb location: (%d, %d)" % (bomb_x, bomb_y)

        # Increment neighbors adjacent bomb counts
        for neighbor in range(numNeighbors):
            next_x = bomb_x + adj_x[neighbor]
            next_y = bomb_y + adj_y[neighbor]
            # Check that neighbor is in room
            if 0 <= next_x < cols and 0 <= next_y < rows:
            #if((next_x >= 0) and (next_x < cols)) and ((next_y >= 0) and (next_y < rows)):
                world_map[next_x][next_y].addAdjBomb()


    # Print out the current map
    for y in range(rows):
        printRow = []
        for x in range(cols):
            printRow.append(world_map[x][y].printBombs())
        print printRow
        
    
    return world_map

# Checks map to ensure there are no closed off areas
def checkMapLegality(world_map):
    
    # DFS to add all non walled neighbors to list then do the same for their neighbors
    # If not on list- regenerate map
    
    pass

class WorldSquare:
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
        self.battery = 0

    def printBombs(self):
        if self.bomb:
            return 'B'
        else:
            return str(self.adjBombs)

    def __str__(self):
        return "%d, %d, %d, %d" % (self.adjBombs, self.adjBats, self.bomb, self.battery)



def main():
    # Command line format: minesweeper.py puzzleHeight puzzleWidth bumbBatteries numBombs
    puzzleHeight = int(sys.argv[1])
    puzzleWidth = int(sys.argv[2])
    numBatteries = int(sys.argv[3])
    numBombs = int(sys.argv[4])
    worldMap = makeMap(puzzleHeight, puzzleWidth, numBatteries, numBombs)


    
sys.argv = ['minesweeper.py', 8, 8, 3, 20]

if __name__ == "__main__":
    main()
