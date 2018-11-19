import pyxel

# Interface to allow the Controller to talk to the Graph.
class ControllerToGraph():
	def __init__(self, graph):
		self.graph = graph
		
	def add_velocity(self, velocity_adjustment):
		self.graph.add_velocity(velocity_adjustment)

# Keeps track of factors that affect the graph's velocity, either from the player or 
# the environment.
class Controller():
	def __init__(self, graph, character_display_reservoir_interface):
		self.reservoir = 0
		#TODO Refactor: Should we create interfaces elsewhere and pass in, or pass and create here?
		self.graph_handle = ControllerToGraph(graph)
		self.character_display_reservoir_handle = character_display_reservoir_interface
		# List of things that are currently affecting the graph.
		self.affectors = []
		
	def update(self):
		for index in range(len(self.affectors) -1, -1, -1):
			affector = self.affectors[index]
			# Here we scale for the "y increases downwards" thing
			self.graph_handle.add_velocity(-affector.get_effect_for_this_tick())
			if (affector.is_finished()):
				self.affectors.remove(affector)
				
		self.character_display_reservoir_handle.empty_down_reservoir()
		for affector in self.affectors:
			self.character_display_reservoir_handle.add_down_reservoir_amount(affector)
			
	def reset(self):
		self.reservoir = 0
		self.affectors = []
			
		
# Interface to allow things (player or environment) to add things that will affect the 
# graph		
class ControllerInterface():
	def __init__(self, controller):
		self.controller = controller
		
	def add_affector(self, affector):
		self.controller.affectors.append(affector)
				
# Represents something that can affect the graphs, whose effect changes with time.
class TimeDependentAffector():
	INFINITE = -1
	def __init__(self, lifetime):
		# if lifetime == 0, effect lasts one tick,
		# if lifetime == TimeDependentAffector.INFINITE, effect lasts forever
		self.lifetime = lifetime
		self.time_elapsed = 0
		
	def is_finished(self):
		return self.time_elapsed > self.lifetime if self.lifetime != TimeDependentAffector.INFINITE else False
		
	# Updates the lifecycle, and returns the effect for this particular tick
	def get_effect_for_this_tick(self):
		self.time_elapsed += 1
		return self.f(self.time_elapsed)
		
	# Can be set or overrided to determine how the effect changes over time.
	def f(self, time):
		return 0
		
		