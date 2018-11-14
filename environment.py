from controller import TimeDependentAffector
from random import randint

class Environment():
	def __init__(self, controller_interface):
		self.controller_interface = controller_interface
		self.controller_interface.add_affector(RandomPerturbationAffector())
		
	def update(self):
		pass
		
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
		