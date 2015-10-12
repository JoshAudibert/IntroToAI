import sys
import minesweeper

def main():
    easy = True
    medium = False
    hard = False

    if easy:
        numBombs = 10
        numBatteries = 10
        puzzleWidth = 9
        puzzleHeight = 9

    if medium:
        numBombs = 40
        numBatteries = 10
        puzzleWidth = 16
        puzzleHeight = 16

    if hard:
        numBombs = 99
        numBatteries = 10
        puzzleWidth = 30
        puzzleHeight = 16

    for i in range(10):
        print "Test ", i
        worldMap = minesweeper.makeMap(puzzleHeight, puzzleWidth, numBatteries, numBombs)
        minesweeper.solve(worldMap)

if __name__ == "__main__":
    main()

