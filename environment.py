from controller import TimeDependentAffector
from line import LineState
from random import randint

class Environment():
	def __init__(self, controller_interface, line_state_interface, threat_interface):
		self.controller_interface = controller_interface
		self.controller_interface.add_affector(RandomPerturbationAffector())
		self.line_state_interface = line_state_interface
		self.threat_interface = threat_interface
		
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
		