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
		self.affectors = []
		
	def update(self):
		for index in range(len(self.affectors) -1, -1, -1):
			affector = self.affectors[index]
			self.graph_handle.add_velocity(affector.get_effect_for_this_tick())
			if (affector.is_finished()):
				self.affectors.remove(affector)
				
class ControllerInterface():
	def __init__(self, controller):
		self.controller = controller
		
	def add_affector(self, affector):
		self.controller.affectors.append(affector)
				
			
class TimeDependentAffector():
	def __init__(self, lifetime):
		self.lifetime = lifetime
		self.time_elapsed = 0
		
	def is_finished(self):
		return self.time_elapsed > self.lifetime
		
	def get_effect_for_this_tick(self):
		self.time_elapsed += 1
		return self.f(self.time_elapsed)
		
	def f(self, time):
		return 0
		
		