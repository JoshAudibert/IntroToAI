from math import ceil
import sys

# class that holds information for 1 node in the search tree
class SearchState:
    def __init__(self, coords, heading, moveSeq, seqCost, score):
        # tuple is x,y
        # top left corner is 0,0
        self.coords = coords
        self.heading = heading
        self.moveSeq = moveSeq # sequence of moves taken to get to this node
        self.seqCost = seqCost
        self.score = score # g(s) + h(s)
        
	# functions used for checking if a node is already in the frontier
    def __eq__(self, other):
        return (self.coords == other.coords and self.heading == other.heading)
    def __ne__(self, other):
        return (self.coords != other.coords or self.heading != other.heading)

# class that holds the map information
class MapInfo:
    def __init__(self, startCoords, goalCoords, terrainMap, selHeuristic):
        self.startCoords = startCoords
        self.goalCoords = goalCoords
        self.terrainMap = terrainMap # list of lists of terrrain complexities
        self.selHeuristic = selHeuristic # which heuristic function to apply
        # x,y coordinate system
        self.height = len(terrainMap[0]) 
        self.width = len(terrainMap)

# parse the command line input, generating a MapInfo object
def parseInput(inputfile, selHeuristic):
    if selHeuristic < 1 or selHeuristic > 6:
        print("Please input a heuristic between 1 and 6 inclusive")
        exit()
    f = open(inputfile, 'r')
    terrainMap = []

    # Get lines from input file
    rows = [str(line).strip().split('\t') for line in f]
    for r in rows:
        terrainMap.append(r)

    # find goal and start nodes, replace with complexity 1
    currRow = 0
    for row in terrainMap:
        currCol = 0
        for i in row:
            if i == 'G':
                terrainMap[currRow][currCol] = 1
                goalCoords = [currCol, currRow]
            elif i == 'S':
                terrainMap[currRow][currCol] = 1
                startCoords = [currCol, currRow]
            else:
                terrainMap[currRow][currCol] = int(i)
            currCol += 1
        currRow += 1

    f.close()

    # convert to x y
    terrainMap = [list(i) for i in zip(*terrainMap)]
    
    return MapInfo(startCoords, goalCoords, terrainMap, selHeuristic)

# computes and returns h(s) for a given state        
def getHeuristic(coords, heading, map_info):
    selHeuristic = map_info.selHeuristic
    
	# determine horizontal and vertical offset from goal
    horizontal = abs(map_info.goalCoords[0] - coords[0])
    vertical = abs(map_info.goalCoords[1] - coords[1])

	# function for calculating the value of heuristic 5
    def getHeuristic5():
        # print "Current: " + str(coords)
        # print "Goal: " + str(map_info.goalCoords)
        heuristic = (horizontal + vertical)
        if heading == 'N' or heading == 'S':
            return heuristic + (horizontal != 0)
        else:
            return heuristic + (vertical != 0)

	# return the value of the appropriate heuristic function
    if selHeuristic == 1:
        return 0
    elif selHeuristic == 2:
        return min(horizontal, vertical)
    elif selHeuristic == 3:
        return max(horizontal, vertical)
    elif selHeuristic == 4:
        return horizontal + vertical
    elif selHeuristic == 5:
        return getHeuristic5()
    else:
        return 3*getHeuristic5()

        
# expand a single node from the frontier, adding its non-duplicate children to the frontier
def expandNode(node, frontierList, expandedStates, map_info):
    frontierList.remove(node)
    expandedStates.append(node)

    # calculate all states 1 move away 
    neighboringStates = []
    if node.heading == 'N':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'E',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'E', map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'W',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'W', map_info)))
        # forward
        if node.coords[1] - 1 >= 0:
            neighboringStates.append(SearchState(
                [node.coords[0], node.coords[1] - 1],
                'N',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] - 1],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] - 1] + getHeuristic((node.coords[0], node.coords[1] - 1), node.heading, map_info)))
        # bash
        if node.coords[1] - 2 >= 0:
            neighboringStates.append(SearchState(
                [node.coords[0], node.coords[1] - 2],
                'N',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0]][node.coords[1] - 2],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0]][node.coords[1] - 2] + getHeuristic((node.coords[0], node.coords[1] - 2), node.heading, map_info)))
    elif node.heading == 'E':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'S',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'S', map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'N',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'N', map_info)))
        # forward
        if node.coords[0] + 1 < map_info.width:
            neighboringStates.append(SearchState(
                [node.coords[0] + 1, node.coords[1]],
                'E',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0] + 1][node.coords[1]],
                node.seqCost + map_info.terrainMap[node.coords[0] + 1][node.coords[1]] + getHeuristic((node.coords[0] + 1, node.coords[1]), node.heading, map_info)))
        # bash
        if node.coords[0] + 2 < map_info.width:
            neighboringStates.append(SearchState(
                [node.coords[0] + 2, node.coords[1]],
                'E',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] + 2][node.coords[1]],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] + 2][node.coords[1]] + getHeuristic((node.coords[0] + 2, node.coords[1]), node.heading, map_info)))
    elif node.heading == 'S':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'W',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'W', map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'E',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'E', map_info)))
        # forward
        if node.coords[1] + 1 < map_info.height:
            neighboringStates.append(SearchState(
                [node.coords[0], node.coords[1] + 1],
                'S',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] + 1],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] + 1] + getHeuristic((node.coords[0], node.coords[1] + 1), node.heading, map_info)))
        # bash
        if node.coords[1] + 2 < map_info.height:
            neighboringStates.append(SearchState(
                [node.coords[0], node.coords[1] + 2],
                'S',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0]][node.coords[1] + 2],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0]][node.coords[1] + 2] + getHeuristic((node.coords[0], node.coords[1] + 2), node.heading, map_info)))
    elif node.heading == 'W':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'N',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'N', map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'S',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, 'S', map_info)))
        # forward
        if node.coords[0] - 1 >= 0:
            neighboringStates.append(SearchState(
                [node.coords[0] - 1, node.coords[1]],
                'W',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0] - 1][node.coords[1]],
                node.seqCost + map_info.terrainMap[node.coords[0] - 1][node.coords[1]] + getHeuristic((node.coords[0] - 1, node.coords[1]), node.heading, map_info)))
        # bash
        if node.coords[0] - 2 >= 0:
            neighboringStates.append(SearchState(
                [node.coords[0] - 2, node.coords[1]],
                'W',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] - 2][node.coords[1]],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] - 2][node.coords[1]] + getHeuristic((node.coords[0] - 2, node.coords[1]), node.heading, map_info)))
    
    # add unique neighbors and neighbors with lower cost to frontier
    # using the __eq__ defined for state
    for state in neighboringStates:
        if state not in expandedStates:
            if state not in frontierList:
                # new state
                frontierList.append(state)
            else:
                # duplicate in Frontier
                stateIndex = frontierList.index(state)
                if state.seqCost < frontierList[stateIndex].seqCost:
                    frontierList[stateIndex] = state  

    # sort frontierList by score (g(s) + h(s))
    frontierList.sort(key=lambda state: state.score)
        
# run the A* search by expanding nodes until the goal appears at the beginning of the sorted frontier
# return the information required for the assignment
def runSearch(map_info):
    frontier = []
    expandedStates = []
    frontier.append(SearchState(map_info.startCoords, 'N', [], 0, getHeuristic(map_info.startCoords, 'N', map_info)))
    solnFound = False
    while solnFound == False:
        if frontier[0].coords == map_info.goalCoords:
            solnFound = True
            return (frontier[0], len(expandedStates))
        else:
            expandNode(frontier[0], frontier, expandedStates, map_info)

# parse the command line inputs, run A*, print the results
def main():
    filename = sys.argv[1]
    selHeuristic = int(sys.argv[2]) # which heuristic function to use
    # read the input file and create the map
    map_info = parseInput(filename, selHeuristic)
    # run the search and save the results
    (finalState, numExpanded) = runSearch(map_info)
    # print results
    print("Score: %d" % (100 - finalState.score))
    print("Number of actions: %d" % len(finalState.moveSeq))
    print("Nodes expanded: %d" % numExpanded)
    print("Moves:")
    for move in finalState.moveSeq:
        print(move)
    
if __name__ == "__main__":
    main()
