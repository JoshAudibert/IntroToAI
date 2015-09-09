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


def parseInput():
	global startCoords 
	startCoords = (2,2)
	global goalCoords
	goalCoords = (1,0)
	global terrainMap
	terrainMap = [[4, 2, 1], [1, 9, 4], [4, 9, 1], [6, 6, 3]]
	#terrainMap = [[4, 1, 4, 6], [2, 9, 9, 6], [1, 4, 1, 3]]
	global selHeuristic
	selHeuristic = 1 # which heuristic function to use
	global mapHeight
	mapHeight = 3
	global mapWidth
	mapWidth = 4
		
def getHeuristic(coords):
	global selHeuristic
	global goalCoords
	
	# use if statements to determine which heuristic to apply
	# return heuristic value for the input coordinates
	if selHeuristic == 1:
		return 0
	elif selHeuristic == 2:
		pass
	else:
		pass
		
	pass
		
def expandNode(node, frontierList):
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
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# turn left
		neighboringStates.append(SearchState(
			node.coords,
			'W',
			node.moveSeq + ['L'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# forward
		if node.coords[1] - 1 >= 0:
			neighboringStates.append(SearchState(
				(node.coords[0], node.coords[1] - 1),
				'N',
				node.moveSeq + ['F'],
				node.seqCost + terrainMap[node.coords[0]][node.coords[1] - 1],
				node.seqCost + terrainMap[node.coords[0]][node.coords[1] - 1] + getHeuristic((node.coords[0], node.coords[1] - 1))))
		# bash
		if node.coords[1] - 2 >= 0:
			neighboringStates.append(SearchState(
				(node.coords[0], node.coords[1] - 2),
				'N',
				node.moveSeq + ['B', 'F'],
				node.seqCost + 3 + terrainMap[node.coords[0] - 2][node.coords[1]],
				node.seqCost + 3 + terrainMap[node.coords[0] - 2][node.coords[1]] + getHeuristic((node.coords[0], node.coords[1] - 2))))
	elif node.heading == 'E':
		# turn right
		neighboringStates.append(SearchState(
			node.coords,
			'S',
			node.moveSeq + ['R'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# turn left
		neighboringStates.append(SearchState(
			node.coords,
			'N',
			node.moveSeq + ['L'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# forward
		if node.coords[0] + 1 < mapWidth:
			neighboringStates.append(SearchState(
				(node.coords[0] + 1, node.coords[1]),
				'E',
				node.moveSeq + ['F'],
				node.seqCost + terrainMap[node.coords[0] + 1][node.coords[1]],
				node.seqCost + terrainMap[node.coords[0] + 1][node.coords[1]] + getHeuristic((node.coords[0] + 1, node.coords[1]))))
		# bash
		if node.coords[0] + 2 < mapWidth:
			neighboringStates.append(SearchState(
				(node.coords[0] + 2, node.coords[1]),
				'E',
				node.moveSeq + ['B', 'F'],
				node.seqCost + 3 + terrainMap[node.coords[0] + 2][node.coords[1]],
				node.seqCost + 3 + terrainMap[node.coords[0] + 2][node.coords[1]] + getHeuristic((node.coords[0] + 2, node.coords[1]))))
	elif node.heading == 'S':
		# turn right
		neighboringStates.append(SearchState(
			node.coords,
			'W',
			node.moveSeq + ['R'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# turn left
		neighboringStates.append(SearchState(
			node.coords,
			'E',
			node.moveSeq + ['L'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# forward
		if node.coords[1] + 1 < mapHeight:
			neighboringStates.append(SearchState(
				(node.coords[0], node.coords[1] + 1),
				'S',
				node.moveSeq + ['F'],
				node.seqCost + terrainMap[node.coords[0]][node.coords[1] + 1],
				node.seqCost + terrainMap[node.coords[0]][node.coords[1] + 1] + getHeuristic((node.coords[0], node.coords[1] + 1))))
		# bash
		if node.coords[1] + 2 < mapHeight:
			neighboringStates.append(SearchState(
				(node.coords[0], node.coords[1] + 2),
				'S',
				node.moveSeq + ['B', 'F'],
				node.seqCost + 3 + terrainMap[node.coords[0]][node.coords[1] + 2],
				node.seqCost + 3 + terrainMap[node.coords[0]][node.coords[1] + 2] + getHeuristic((node.coords[0], node.coords[1] + 2))))
	elif node.heading == 'W':
		# turn right
		neighboringStates.append(SearchState(
			node.coords,
			'N',
			node.moveSeq + ['R'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# turn left
		neighboringStates.append(SearchState(
			node.coords,
			'S',
			node.moveSeq + ['L'],
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0),
			node.seqCost + ceil(terrainMap[node.coords[0]][node.coords[1]]/3.0) + getHeuristic(node.coords)))
		# forward
		if node.coords[0] - 1 >= 0:
			neighboringStates.append(SearchState(
				(node.coords[0] - 1, node.coords[1]),
				'W',
				node.moveSeq + ['F'],
				node.seqCost + terrainMap[node.coords[0] - 1][node.coords[1]],
				node.seqCost + terrainMap[node.coords[0] - 1][node.coords[1]] + getHeuristic((node.coords[0] - 1, node.coords[1]))))
		# bash
		if node.coords[0] - 2 >= 0:
			neighboringStates.append(SearchState(
				(node.coords[0] - 2, node.coords[1]),
				'W',
				node.moveSeq + ['B', 'F'],
				node.seqCost + 3 + terrainMap[node.coords[0] - 2][node.coords[1]],
				node.seqCost + 3 + terrainMap[node.coords[0] - 2][node.coords[1]] + getHeuristic((node.coords[0] - 2, node.coords[1]))))
	
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
		
def runSearch():
	frontier = list()
	global startCoords
	global goalCoords
	global expandedStates
	expandedStates = list()
	frontier.append(SearchState(startCoords, 'N', list(), 0, getHeuristic(startCoords)))
	solnFound = False
	while solnFound == False:
		if frontier[0].coords == goalCoords:
			solnFound = True
			return frontier[0].moveSeq
		else:
			expandNode(frontier[0], frontier)
		
def main():
	parseInput()
	moveList = runSearch()
	print "Soln:"
	print moveList
	
if __name__ == "__main__":
	main()