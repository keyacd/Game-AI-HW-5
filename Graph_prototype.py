class Graph(object):
	"""General graph prototype"""
	def __init__(self):
		super(Graph, self).__init__()
	def getAdjacent(self, pos):
		"""Get all nodes adjacent to pos in the graph"""
		pass
	def getHeuristicDist(self, start, end):
		"""Get the heuristic distance between the nodes start and end in the graph"""
		pass
	def getEdgeCost(self, n1, n2):
		"""Get edge cost from node n1 to n2"""
		pass
	def getPositions(self):
		"""Return a list of all nodes in the graph"""
		pass
