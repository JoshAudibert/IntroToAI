import sys
import minesweeper

def main():
    easy = False
    medium = True
    hard = False

    if easy:
        numBombs = 10
        numBatteries = 10
        puzzleWidth = 9
        puzzleHeight = 9
    if medium:
        numBombs = 20
        numBatteries = 10
        puzzleWidth = 12
        puzzleHeight = 12
    if hard:
        numBombs = 99
        numBatteries = 10
        puzzleWidth = 30
        puzzleHeight = 16

    for i in range(10):
        print "Test ", i
        worldMap = minesweeper.makeMap(puzzleHeight, puzzleWidth, numBatteries, numBombs)
        while(minesweeper.checkMap(worldMap)):
            worldMap = minesweeper.makeMap(puzzleHeight, puzzleWidth, numBatteries, numBombs)
        minesweeper.solve(worldMap)

if __name__ == "__main__":
    main()

    
