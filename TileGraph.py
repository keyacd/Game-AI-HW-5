class TileGraph(object):
	"""Graph definition for tile map"""
	def __init__(self, tiled_map):
		super(TileGraph, self).__init__()
		self.tiled_map = tiled_map
		self.width = len(tiled_map)
		self.height = len(tiled_map[0])
	def getAdjacent(self, pos):
		"""Get all nodes adjacent to pos in the graph"""
		potential_adjacent = [(-1, 0), (0, 1), (1, 0), (0, -1)]
		adjacent = []
		for p in potential_adjacent:
			cur = (pos[0] + p[0], pos[1] + p[1])
			if cur[0] < 0 or cur[1] < 0 or cur[0] >= self.width or cur[1] >= self.height:
				continue
			if self.tiled_map[cur[1]][cur[0]].open:
				adjacent.append((cur[0], cur[1]))
		return adjacent
	def getHeuristicDist(self, start, end):
		"""Get the heuristic distance between the nodes start and end in the graph"""
		return abs(start[0] - end[0]) + abs(start[1] - end[1])
	def getEdgeCost(self, n1, n2):
		"""Get edge cost from node n1 to n2"""
		return 1
	def getPositions(self):
		"""Return a list of all nodes in the graph"""
		positions = []
		for i in range(self.width):
			for j in range(self.height):
				positions.append((i, j))
		return positions

		