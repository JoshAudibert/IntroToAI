from random import randint
from robot import Robot
from robot import RobotSquare
from robot import RobotMap
import time
import sys
from util import debug
from util import analysis

def solve(worldMap):
    # Make instance of robot
    initialBattery = 20
    m_robot = Robot(initialBattery, worldMap.getStartingSquare().loc, worldMap.rows, worldMap.cols)
    # tell robot about world map info of its starting location
    m_robot.move(worldMap.getStartingSquare())
    
    bot_running = True
    # while robot not dead and not finished exploring
    while bot_running:
        # ask robot where it wants to move
        move_to = m_robot.chooseNextLocation().loc
        print "Move to:", move_to
        # tell robot what happens when it moves to its new location
        m_robot.move(worldMap.getSquare(move_to))
        # check if the robot is dead or done exploring
        if m_robot.isDead or len(m_robot.robotMap.fringe) == 0:
            # break loop
            bot_running = False
    
    printAnalysis(m_robot, worldMap)

# return / print statistics of robot performance
def printAnalysis(robot, worldMap):
    numTotalSafeSquares = (worldMap.rows * worldMap.cols) - worldMap.numBombs
    numCheckedSquares = len(robot.robotMap.checkedSquares)

    if robot.isDead:
        print "The robot searched %s/%s safe squares" % (str(numCheckedSquares-1), str(numTotalSafeSquares))
        if robot.battery:
            print "THE ROBOT EXPLODED AT LOCATION %s!" % str(robot.loc)
        else:
            print "THE ROBOT RAN OUT OF BATTERY AT LOCATION %s" % str(robot.loc)
    else:
        print "THE ROBOT RAN OUT OF FRINGE"

    print "***Actual World Map:"
    worldMap.printMap()


def makeMap(rows, cols, numBats, numBombs):

    world_map = []

    # Neighboring Coordinates
    numNeighbors = 8
    # (-1,-1) (0,-1) (1,-1)
    # (-1, 0) robot  (1, 0)
    # (-1, 1) (0, 1) (1, 1)
    adj_x = [-1,0,1,-1,1,-1,0,1]
    adj_y = [-1,-1,-1,0,0,1,1,1]

    # Randomly pick a starting location for the robot
    startingLoc = [randint(0, cols-1), randint(0, rows-1)]

    # List to hold all of the world map pieces
    world_map = [[WorldSquare([x, y],0,0,True,0) for y in range(rows)] for x in range(cols)]
    
    # Calculate the number of safe squares needed
    safeSum = rows*cols - numBombs
    safeCount = 0

    # Ensure that the starting location is not a bomb
    world_map[startingLoc[0]][startingLoc[1]].removeBomb()
    safeCount += 1

    # Keep track of all coordinates of items in the fringe
    fringe_x = []
    fringe_y = []

    # Make all 9 squares bordering start safe
    for neighbor in range(numNeighbors):
        next_x = startingLoc[0] + adj_x[neighbor]
        next_y = startingLoc[1] + adj_y[neighbor]
        # Check that neighbor is in room
        if 0 <= next_x < cols and 0 <= next_y < rows:
            # Check that neighbor is not safe already
            if world_map[next_x][next_y].bomb:
                world_map[next_x][next_y].removeBomb()
                safeCount += 1
                fringe_x.append(next_x)
                fringe_y.append(next_y)

    # Move from start randomly until all safe squares are placed
    curr_x = startingLoc[0]
    curr_y = startingLoc[1]

    # Keep going until all safe squares are placed
    while safeCount != safeSum:
        # Randomly pick a square from the fringe
        nextStep = randint(0,len(fringe_x) - 1)
        curr_x = fringe_x[nextStep]
        curr_y = fringe_y[nextStep]
        # Randomly pick a direction to move in
        direction = randint(0,7)
        next_x = curr_x + adj_x[direction]
        next_y = curr_y + adj_y[direction]
        # Check that neighbor is in room
        if 0 <= next_x < cols and 0 <= next_y < rows:
            # Check that neighbor is not safe already
            if world_map[next_x][next_y].bomb:
                world_map[next_x][next_y].removeBomb()
                safeCount += 1
                fringe_x.append(next_x)
                fringe_y.append(next_y)

    startingMap = WorldMap(world_map, startingLoc, numBombs, numBats, rows, cols)
     # update adjacent bomb counts
    for r in range(rows):
        for c in range(cols):
            if world_map[c][r].bomb:
                neighbors = startingMap.getNeighbors([c, r])
                for neighbor in neighbors:
                    if not neighbor.bomb:
                        neighbor.addAdjBomb()
    startingMap.printMap()

    analysis("Safe squares = " + str(safeCount))
    analysis("Numb bombs = " + str(numBombs))
    return startingMap


# Class to hold all of the pieces of the world map
class WorldMap:
    def __init__(self, worldSquares, startingLocation, numBombs, numBatteries, rows, cols):
        self.worldSquares = worldSquares  # list of all world map pieces
        self.startLoc = startingLocation
        self.numBombs = numBombs
        self.numBatteries = numBatteries
        self.rows = rows
        self.cols = cols

    # Print out the current map
    def printMap(self):
        for y in range(self.rows):
            printRow = []
            for x in range(self.cols):
                printRow.append(self.worldSquares[x][y].printBombs())
            print printRow

    def mapSize(self):
        size = self.rows*self.cols
        analysis(size)

    def removeBat(self, loc):
        self.worldSquares[loc[0]][loc[1]].removeBattery()
        neighbors = self.getNeighbors(loc)
        for n in range(len(neighbors)):
            neighbors[n].removeAdjBat

    # find all neighbors within the map
    def getNeighbors(self, loc):    
        delta_x = [-1, 0, 1,-1, 1,-1, 0, 1]
        delta_y = [-1,-1,-1, 0, 0, 1, 1, 1]
        neighbors = []
        for i in range(len(delta_x)):
            new_x = loc[0] + delta_x[i]
            new_y = loc[1] + delta_y[i]
            if 0 <= new_x < self.cols and 0 <= new_y < self.rows:
                neighbors.append(self.worldSquares[new_x][new_y])
        return neighbors

    def getStartingSquare(self):
        return self.worldSquares[self.startLoc[0]][self.startLoc[1]]
        
    def getSquare(self, loc):
        return self.worldSquares[loc[0]][loc[1]]
    

class WorldSquare:
    def __init__(self, location, adjBombs, adjBats, bomb, battery):
        self.loc = location
        self.adjBombs = adjBombs
        self.adjBats = adjBats
        self.bomb = bomb 
        self.battery = battery # 0 if no battery, integer for amount of charge

    def removeBattery(self):
        self.battery = False

    def removeAdjBat(self):
        if self.adjBats > 0:
            self.adjBats -= 1

    def addAdjBat(self):
        self.adjBats += 1

    def addAdjBomb(self):
        self.adjBombs += 1

    def placeBomb(self):
        self.bomb = True

    def removeBomb(self):
        self.bomb = False

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
    # move to lowest probability of a bomb in fringe break ties  sort list
    solve(worldMap)
    
sys.argv = ['minesweeper.py', 8, 8, 3, 10]

if __name__ == "__main__":
    main()
