import pyxel
from typing import Any

# Represents something that can affect the graphs, whose effect changes with time.
class TimeDependentAffector():
	INFINITE = -1
	def __init__(self, lifetime : int) -> None:
		# if lifetime == 0, effect lasts one tick,
		# if lifetime == TimeDependentAffector.INFINITE, effect lasts forever
		self.lifetime = lifetime
		self.time_elapsed = 0

	def is_finished(self) -> bool:
		return self.time_elapsed > self.lifetime if self.lifetime != TimeDependentAffector.INFINITE else False

	def reset(self) -> None:
		self.time_elapsed = 0

	# Updates the lifecycle, and returns the effect for this particular tick
	def get_effect_for_this_tick(self) -> float:
		self.time_elapsed += 1
		return self.f(self.time_elapsed)

	# Can be used to work out how much for this affector will deliver before finishing
	def remaining_affect(self) -> float:
		return 0

	# Can be set or overrided to determine how the effect changes over time.
	def f(self, time : int) -> float:
		return 0

# Keeps track of factors that affect the graph's velocity, either from the player or
# the environment.
class Controller():
	def __init__(self, line_interface : Any) -> None:
		self.line_interface = line_interface
		self.reservoir = 0
		# List of things that are currently affecting the graph.
		self.affectors : list[TimeDependentAffector] = []

	def set_character_display_reservoir_interface(self, character_display_reservoir_interface : Any) -> None:
		self.character_display_reservoir_handle = character_display_reservoir_interface

	def update(self) -> None:
		for index in range(len(self.affectors) -1, -1, -1):
			affector = self.affectors[index]
			# Here we scale for the "y increases downwards" thing
			self.line_interface.add_velocity(-affector.get_effect_for_this_tick())
			if (affector.is_finished()):
				self.affectors.remove(affector)

		self.character_display_reservoir_handle.empty_down_reservoir()
		for affector in self.affectors:
			self.character_display_reservoir_handle.add_down_reservoir_amount(affector.remaining_affect())

	def reset(self) -> None:
		self.reservoir = 0
		self.affectors = []


# Interface to allow things (player or environment) to add things that will affect the
# graph
class ControllerInterface():
	def __init__(self, controller : Controller) -> None:
		self.controller = controller

	def add_affector(self, affector : TimeDependentAffector) -> None:
		self.controller.affectors.append(affector)
