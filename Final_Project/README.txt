# IntroToAI
# Final Project

NOTE: Python 2.7 was used to write and run this program,
	it will most likely not run with python 3

This program is designed to run a version of a minesweeper game.
The minesweeper game includes a path cost and the robot needs 
battery life in order to make moves. The robot starts off with
some battery life and can win the game by marking where all of 
the bombs are without running into a bomb or running out of 
battery life.

The program can be run in command line by:

minesweeper.py puzzleHeight puzzleWidth numBats numBombs

Example running minesweeper with a 10x10 board with 5 batteries and 15 bombs

minesweeper.py 10 10 5 15

Argv[0]: minesweeper.py
Argv[1]: puzzle height
Argv[2]: puzzle width
Argv[3]: number of batteries to be placed on the board
Argv[4]: number of bombs to be placed on the board
