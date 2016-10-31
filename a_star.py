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
		for pos in openSet:
			key = pos
			val = scores[key]
			if val < lowest_val:
				lowest = key
				lowest_val = val
		return lowest
	def reconstruct_path(cameFrom, end):
		path = [end]
		cur = end
		while cur in cameFrom:
			cur = cameFrom[cur]
			path.append(cur)
		path.reverse()
		return path
	
	while len(openSet) > 0:
		current = get_lowest_fScore(fScore)
		neighbors = graph.getAdjacent(current)
		
		openSet.remove(current)
		closedSet.add(current)
		if current == end:
			yield reconstruct_path(cameFrom, current)
			return
		yield current
		
		for neighbor in neighbors:
			if neighbor in closedSet:
				continue
			tentative_g_score = gScore[current] + graph.getEdgeCost(current, neighbor)
			if neighbor not in openSet:
				openSet.add(neighbor)
			elif tentative_g_score >= gScore[neighbor]:
				continue
			
			cameFrom[neighbor] = current
			gScore[neighbor] = tentative_g_score
			fScore[neighbor] = gScore[neighbor] + graph.getHeuristicDist(neighbor, end)