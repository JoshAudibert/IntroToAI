from math import ceil

class SearchState:
    def __init__(self, coords, heading, moveSeq, seqCost, score):
        # tuple is x,y
        # top left corner is 0,0
        self.coords = coords
        self.heading = heading
        self.moveSeq = moveSeq
        self.seqCost = seqCost
        self.score = score
        
    def __eq__(self, other):
        return self.coords == other.coords and self.heading == other.heading
    def __ne__(self, other):
        return self.coords != other.coords or self.heading != other.heading


class MapInfo:
    def __init__(self, startCoords, goalCoords, terrainMap):
        self.startCoords = startCoords
        self.goalCoords = goalCoords
        self.terrainMap = terrainMap
        # x,y coordinate system
        self.height = len(terrainMap[0]) 
        self.width = len(terrainMap)


def parseInput(inputfile):
    f = open(inputfile, 'r')
    terrainMap = []

    # Get lines from input file
    rows = [str(line).strip().split('\t') for line in f]
    for r in rows:
        terrainMap.append(list(r))

    currRow = 0
    for row in terrainMap:
        currCol = 0
        for i in row:
            if i == 'G':
                terrainMap[currRow][currCol] = 1
                goalCoords = (currCol, currRow)
            elif i == 'S':
                terrainMap[currRow][currCol] = 1
                startCoords = (currCol, currRow)
            else:
                terrainMap[currRow][currCol] = int(i)
            currCol += 1
        currRow += 1

    f.close()
    print(terrainMap)

    # convert to x y
    temp = []
    temp = [list(i) for i in zip(*terrainMap)]
    terrainMap = temp
    print(terrainMap)
    
    # NOTE: map coordinates are x,y
    global selHeuristic # which heuristic function to use
    selHeuristic = 1
    
    return MapInfo(startCoords, goalCoords, terrainMap)

        
def getHeuristic(coords, map_info):
    global selHeuristic
    
    # use if statements to determine which heuristic to apply
    # return heuristic value for the input coordinates
    if selHeuristic == 1:
        return 0
    elif selHeuristic == 2:
        pass
    else:
        pass
        
    pass
        
def expandNode(node, frontierList, expandedStates, map_info):
    frontierList.remove(node)
    expandedStates.append(node)
    # print "Node:"
    # print node.moveSeq
    # print node.coords
    # print node.heading
    # print node.seqCost

    # calculate all states 1 move away 
    neighboringStates = []
    if node.heading == 'N':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'E',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'W',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # forward
        if node.coords[1] - 1 >= 0:
            neighboringStates.append(SearchState(
                (node.coords[0], node.coords[1] - 1),
                'N',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] - 1],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] - 1] + getHeuristic((node.coords[0], node.coords[1] - 1), map_info)))
        # bash
        if node.coords[1] - 2 >= 0:
            neighboringStates.append(SearchState(
                (node.coords[0], node.coords[1] - 2),
                'N',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] - 2][node.coords[1]],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] - 2][node.coords[1]] + getHeuristic((node.coords[0], node.coords[1] - 2), map_info)))
    elif node.heading == 'E':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'S',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'N',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # forward
        if node.coords[0] + 1 < map_info.width:
            neighboringStates.append(SearchState(
                (node.coords[0] + 1, node.coords[1]),
                'E',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0] + 1][node.coords[1]],
                node.seqCost + map_info.terrainMap[node.coords[0] + 1][node.coords[1]] + getHeuristic((node.coords[0] + 1, node.coords[1]), map_info)))
        # bash
        if node.coords[0] + 2 < map_info.width:
            neighboringStates.append(SearchState(
                (node.coords[0] + 2, node.coords[1]),
                'E',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] + 2][node.coords[1]],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] + 2][node.coords[1]] + getHeuristic((node.coords[0] + 2, node.coords[1]), map_info)))
    elif node.heading == 'S':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'W',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'E',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # forward
        if node.coords[1] + 1 < map_info.height:
            neighboringStates.append(SearchState(
                (node.coords[0], node.coords[1] + 1),
                'S',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] + 1],
                node.seqCost + map_info.terrainMap[node.coords[0]][node.coords[1] + 1] + getHeuristic((node.coords[0], node.coords[1] + 1), map_info)))
        # bash
        if node.coords[1] + 2 < map_info.height:
            neighboringStates.append(SearchState(
                (node.coords[0], node.coords[1] + 2),
                'S',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0]][node.coords[1] + 2],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0]][node.coords[1] + 2] + getHeuristic((node.coords[0], node.coords[1] + 2), map_info)))
    elif node.heading == 'W':
        # turn right
        neighboringStates.append(SearchState(
            node.coords,
            'N',
            node.moveSeq + ['R'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # turn left
        neighboringStates.append(SearchState(
            node.coords,
            'S',
            node.moveSeq + ['L'],
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0),
            node.seqCost + ceil(map_info.terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords, map_info)))
        # forward
        if node.coords[0] - 1 >= 0:
            neighboringStates.append(SearchState(
                (node.coords[0] - 1, node.coords[1]),
                'W',
                node.moveSeq + ['F'],
                node.seqCost + map_info.terrainMap[node.coords[0] - 1][node.coords[1]],
                node.seqCost + map_info.terrainMap[node.coords[0] - 1][node.coords[1]] + getHeuristic((node.coords[0] - 1, node.coords[1]), map_info)))
        # bash
        if node.coords[0] - 2 >= 0:
            neighboringStates.append(SearchState(
                (node.coords[0] - 2, node.coords[1]),
                'W',
                node.moveSeq + ['B', 'F'],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] - 2][node.coords[1]],
                node.seqCost + 3 + map_info.terrainMap[node.coords[0] - 2][node.coords[1]] + getHeuristic((node.coords[0] - 2, node.coords[1]), map_info)))
    
    # add unique neighbors and neighbors with lower cost to frontier
    # implementation depends on in, index, and remove functions using the __eq__ defined for state, not sure if they do
    for state in neighboringStates:
        if state in expandedStates:
            try:
                stateIndex = expandedStates.index(state)
                if state.seqCost < expandedStates[stateIndex].seqCost:
                    # print "replace state"
                    # print expandedStates[stateIndex].moveSeq
                    # print expandedStates[stateIndex].coords
                    # print expandedStates[stateIndex].heading
                    # print "new state"
                    # print state.moveSeq
                    # print state.coords
                    # print state.heading
                    expandedStates.remove(state) #remove the old one at stateIndex?
                    expandedStates.append(state)
                    frontierList.append(state)                  
            except:
                print "state index not found"
            pass
        else:
            frontierList.append(state)
            
    # sort frontierList by score (cost + heuristic)
    frontierList.sort(key=lambda state: state.score)
    pass
        
def runSearch(map_info):
    frontier = list()
    expandedStates = list()
    frontier.append(SearchState(map_info.startCoords, 'N', list(), 0, getHeuristic(map_info.startCoords, map_info)))
    solnFound = False
    while solnFound == False:
        if frontier[0].coords == map_info.goalCoords:
            solnFound = True
            return frontier[0].moveSeq
        else:
            expandNode(frontier[0], frontier, expandedStates, map_info)
        
def main():
    map_info = parseInput('assignment 1, sample board.txt')
    moveList = runSearch(map_info)
    print("Soln:")
    print(moveList)
    
if __name__ == "__main__":
    main()
