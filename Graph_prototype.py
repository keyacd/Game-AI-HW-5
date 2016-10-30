class Graph(object):
	"""General graph prototype"""
	def __init__(self):
		super(Graph, self).__init__()
	def getAdjacent(self, pos):
		"""Get all adjacent nodes in the graph"""
		pass
	def getHeuristicDist(self, start, end):
		"""Get the heuristic distance between tow nodes start and end in the graph"""
		pass
	def getPositions(self):
		"""Return a list of all nodes in the graph"""
		pass
