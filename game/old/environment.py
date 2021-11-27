from plugins.sprite import TextSprite
from controller import TimeDependentAffector
from line import LineState
from random import randint, random, choice
from typing import Any, Callable, Mapping

# Controls the environmental effects on the line. Essentially the enemy of the player.
class Environment():
	def __init__(self, controller_interface : Any, threat_interface : Any, line_state_interface : Any) -> None:
		self.controller_interface = controller_interface
		self.controller_interface.add_affector(RandomPerturbationAffector())
		self.threat_interface = threat_interface
		self.line_state_interface = line_state_interface
		# time before first Event
		self.count = randint(200, 300)

		# Possible events that exclusively push the line down
		self.DOWN_EVENTS = {
			"Chasing Criminal" : SlowStartStopAffector(1400, 300, False),
			"No Time To Rest!" : SlowStartStopAffector(900, 400, False),
			"Difficult Fight"  : SlowStartStopAffector(1500, 100, False)
		}
		# Weight assigned to down events in weighted random selection
		self.num_down = 10

		# Possible events that exclusively push the line up
		self.UP_EVENTS = {
			"Time Pressure"                : SlowStartStopAffector(1500, 300, True),
			"Exposure To High Temperature" : SlowStartStopAffector(1200, 400, True),
			"Refuelling"                   : SlowStartStopAffector(1400, 200, True)
		}
		# Weight assigned to up events in weighted random selection
		self.num_up = 10

		# Possible events that have a more complex effect on the line
		self.SPECIAL_EVENTS = {"Poisoned": UpDownAffector(250, 500, 0.7, 1.7, self.controller_interface, True)}
		# Weight assigned to special events in weighted random selection
		self.num_special = 2

	def set_character_display_text_interface(self, character_display_text_interface : Any) -> None:
		self.character_display_text_interface = character_display_text_interface

	def reset(self) -> None:
		self.controller_interface.add_affector(RandomPerturbationAffector())

	def update(self) -> None:
		current_line_state = self.line_state_interface.get_current_line_state()
		if current_line_state == LineState.STATE_NORMAL:
			self.threat_interface.adjust_threat_percent(-0.3 / 100)
		elif current_line_state == LineState.STATE_HIGH:
			self.threat_interface.adjust_threat_percent(0.2 / 100)
		elif current_line_state == LineState.STATE_LOW:
			self.threat_interface.adjust_threat_percent(1 / 100)

		self.count -= 1
		if not self.count:
			event_list = self.pick_random_event_list()
			name = choice(list(event_list.keys()))
			self.character_display_text_interface.add_text(TextSprite(name, 7), 30)
			event = event_list[name]
			event.reset()
			self.controller_interface.add_affector(event)
			self.count = self.set_timer()

	# Picks random event list based on weighting
	#TODO Investigate: Consider implementing weighted random options as plugin.
	def pick_random_event_list(self) -> Mapping[str, TimeDependentAffector]:
		total = self.num_down + self.num_up + self.num_special
		self.chance_down = self.num_down / total
		self.chance_up = self.chance_down + self.num_up / total
		selection_num = random()
		if selection_num < self.chance_down:
			return self.DOWN_EVENTS
		elif selection_num < self.chance_up:
			return self.UP_EVENTS
		else:
			return self.SPECIAL_EVENTS

	# Time between events
	def set_timer(self) -> int:
		return randint(300, 600)


# Affector that eases in and out of an effect, pushing either up or down
class SlowStartStopAffector(TimeDependentAffector):
	def __init__(self, severity : float, lifetime : int, pushing_up : bool) -> None:
		super(SlowStartStopAffector, self).__init__(lifetime)
		self.severity = severity
		self.pushing_up = pushing_up

	def f(self, time : int) -> float:
		abs_val = self.severity * self.curve(time / self.lifetime) / self.lifetime
		return abs_val if self.pushing_up else -abs_val

	def curve(self, percent_time : float) -> float:
		return percent_time*percent_time*(1-percent_time)*(1-percent_time)

# Twin of the UpDownAffector, represents the second portion of that effect.
class InverseAffector(TimeDependentAffector):
	def __init__(self, severity : float, lifetime : int, curve_func : Callable[[float], float]) -> None:
		super(InverseAffector, self).__init__(lifetime)
		self.severity = severity
		self.curve = curve_func

	def f(self, time : int) -> float:
		return -self.severity * self.curve(time / self.lifetime) / self.lifetime

# Affector that pushes the line first in one direction then the other, by spawning the
# inverse affector at the end of its life.
class UpDownAffector(TimeDependentAffector):
	def __init__(self, severity : float, lifetime : int, change_point : float, severity_difference : float, controller_interface : Any, up_initially : bool) -> None:
		super(UpDownAffector, self).__init__(int(lifetime * change_point))
		self.controller_interface = controller_interface
		self.inverse_lifetime = int(lifetime * (1 - change_point))
		self.severity_difference = severity_difference
		self.severity = severity
		self.curve = self.up_curve if up_initially else lambda x: -self.up_curve(x)

	def f(self, time : int) -> float:
		if self.is_finished():
			self.add_inverse_affector()
		return self.severity * self.curve(time / self.lifetime) / self.lifetime

	def up_curve(self, percent_time : float) -> float:
		return percent_time*(1-percent_time)

	def add_inverse_affector(self) -> None:
		inverse_affector = InverseAffector(self.severity * self.severity_difference, self.inverse_lifetime, self.curve)
		self.controller_interface.add_affector(inverse_affector)

# Causes random movements in the line, gives it some life.
class RandomPerturbationAffector(TimeDependentAffector):
	def __init__(self) -> None:
		super(RandomPerturbationAffector, self).__init__(-1)
		self.count = self.set_timer()

	def f(self, time : int) -> float:
		self.count -= 1
		if not self.count:
			# How far to move
			val = randint(1,2)
			pos = randint(0,1)
			self.count = self.set_timer()
			return val if pos else -val
		return 0

	def set_timer(self) -> int:
		# Time between movements
		return randint(10,50)
