import sys
import minesweeper

def main():
    numBombs = 10
    numBatteries = 10
    puzzleWidth = 10
    puzzleHeight = 10

    for i in range(10):
        print "Test ", i
        worldMap = minesweeper.makeMap(puzzleHeight, puzzleWidth, numBatteries, numBombs)
        minesweeper.solve(worldMap)

if __name__ == "__main__":
    main()

    
