import math
class WaypointGraph(object):
	"""Graph definition for tile map"""
	def __init__(self, waypoints):
		super(WaypointGraph, self).__init__()
		self.waypoints = waypoints
	def getAdjacent(self, pos):
		"""Get all nodes adjacent to pos in the graph"""
		return self.waypoints[pos]
	def getHeuristicDist(self, start, end):
		"""Get the heuristic distance between the nodes start and end in the graph"""
		return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
	def getEdgeCost(self, n1, n2):
		"""Get edge cost from node n1 to n2"""
		return math.sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)
	def getPositions(self):
		"""Return a list of all nodes in the graph"""
		return self.waypoints.keys()

		