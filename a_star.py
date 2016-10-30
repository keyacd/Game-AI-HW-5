def a_star_pathfind(graph, start, end):
	closedSet = set()
	openSet = set([start])
	
	gScore = {}
	fScore = {}
	for pos in graph.getPositions():
		gScore[pos] = float("inf")
		fScore[pos] = float("inf")
	cameFrom = {}
	gScore[start] = 0
	fScore[start] = graph.getHeuristicDist(start, end)
	
	def get_lowest_fScore(scores):
		lowest = None
		lowest_val = float("inf")
		for key, val in scores.items():
			if val < lowest_val:
				lowest = key
				lowest_val = val
		return lowest, lowest_val
	def reconstruct_path(cameFrom, end):
		path = [end]
		cur = end
		while cameFrom[cur] != None:
			cur = cameFrom[cur]
			path.append(cur)
		path.reverse()
		return path
	
	while len(openSet) > 0:
		current = get_lowest_fScore(fScore)
		neighbors = getAdjacentOpen()
		
		openSet.remove(current)
		closedSet.add(current)
		if current == goal:
			yield reconstruct_path(cameFrom, current)
			return
		
		for neighbor in neighbors:
			if neighbor in closedSet:
				continue
			tentative_g_score = gScore[current] + graph.getEdgeCost(current, n)
			if neighbor not in openSet:
				openSet.add(neighbor)
				yield neighbor
			elif tentative_g_score >= gScore[neighbor]:
				continue
			
			cameFrom[neighbor] = current
			gScore[neighbor] = tentative_g_score
			fScore[neighbor] = gScore[neighbor] + graph.getHeuristicDist(neighbor, goal)