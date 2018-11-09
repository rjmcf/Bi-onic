import pyxel

class ControllerToGraph():
	def __init__(self, graph):
		self.graph = graph
		
	def add_velocity(self, velocity_adjustment):
		self.graph.add_velocity(velocity_adjustment)


class Controller():
	def __init__(self, graph):
		self.reservoir = 0
		self.graph_handle = ControllerToGraph(graph)
		
	def update(self):
		if pyxel.btn(pyxel.KEY_UP):
			self.graph_handle.add_velocity(-0.1)
		elif pyxel.btn(pyxel.KEY_DOWN):
			self.graph_handle.add_velocity(0.1)