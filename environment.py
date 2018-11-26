from controller import TimeDependentAffector
from line import LineState
from random import randint, random, choice

class Environment():
	def __init__(self, controller_interface, threat_interface, line_state_interface):
		self.controller_interface = controller_interface
		self.controller_interface.add_affector(RandomPerturbationAffector())
		self.threat_interface = threat_interface
		self.line_state_interface = line_state_interface
		self.count = randint(200, 300)
		self.DOWN_EVENTS = {"High Exertion" : SlowStartStopAffector(1300, 100, False)}
		self.num_down = 10
		self.UP_EVENTS = {"Time Pressure" : SlowStartStopAffector(1500, 300, True)}
		self.num_up = 10
		self.SPECIAL_EVENTS = {"Poisoned": UpDownAffector(250, 500, 0.7, 1.7, self.controller_interface, True)}
		self.num_special = 2
			
	def reset(self):
		self.controller_interface.add_affector(RandomPerturbationAffector())
		
	def update(self):
		current_line_state = self.line_state_interface.get_current_line_state()
		if current_line_state == LineState.STATE_NORMAL:
			self.threat_interface.adjust_threat_percent(-0.3 / 100)
		elif current_line_state == LineState.STATE_HIGH:
			self.threat_interface.adjust_threat_percent(0.1 / 100)
		elif current_line_state == LineState.STATE_LOW:
			self.threat_interface.adjust_threat_percent(0.5 / 100)
			
		self.count -= 1
		if not self.count:
			event_list = self.pick_random_event_list()
			name = choice(list(event_list.keys()))
			print(name, "chosen!")
			event = event_list[name]
			event.reset()
			self.controller_interface.add_affector(event)
			self.count = self.set_timer()			
			
	def pick_random_event_list(self):
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
			
	def set_timer(self):
		return randint(400, 800)
			
class SlowStartStopAffector(TimeDependentAffector):
	def __init__(self, severity, lifetime, pushing_up):
		super(SlowStartStopAffector, self).__init__(lifetime)
		self.severity = severity
		self.pushing_up = pushing_up
		
	def f(self, time):
		abs_val = self.severity * self.curve(time / self.lifetime) / self.lifetime
		return abs_val if self.pushing_up else -abs_val
		
	def curve(self, percent_time):
		return percent_time*percent_time*(1-percent_time)*(1-percent_time)
		
class UpDownAffector(TimeDependentAffector):
	def __init__(self, severity, lifetime, change_point, severity_difference, controller_interface, up_initially):
		super(UpDownAffector, self).__init__(lifetime * change_point)
		self.controller_interface = controller_interface
		self.inverse_lifetime = lifetime * (1 - change_point)
		self.severity_difference = severity_difference
		self.severity = severity
		self.curve = self.up_curve if up_initially else lambda x: -self.up_curve(x)
		
	def f(self, time):
		if self.is_finished():
			self.add_inverse_affector()
		return self.severity * self.curve(time / self.lifetime) / self.lifetime
	
	def up_curve(self, percent_time):
		return percent_time*(1-percent_time)
		
	def add_inverse_affector(self):
		inverse_affector = InverseAffector(self.severity * self.severity_difference, self.inverse_lifetime, self.curve)
		self.controller_interface.add_affector(inverse_affector)
		
	
class InverseAffector(TimeDependentAffector):
	def __init__(self, severity, lifetime, curve_func):
		super(InverseAffector, self).__init__(lifetime)
		self.severity = severity
		self.curve = curve_func
			
	def f(self, time):
		return -self.severity * self.curve(time / self.lifetime) / self.lifetime
			
class RandomPerturbationAffector(TimeDependentAffector):
	def __init__(self):
		super(RandomPerturbationAffector, self).__init__(-1)
		self.count = self.set_timer()
		
	def f(self, time):
		self.count -= 1
		if not self.count:
			val = randint(1,2)
			pos = randint(0,1)
			self.count = self.set_timer()
			return val if pos else -val
		return 0
		
	def set_timer(self):
		return randint(10,50)
		