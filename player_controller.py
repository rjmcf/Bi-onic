import pyxel
from controller import TimeDependentAffector

# Used by the Player to have an effect on the graph.
class PlayerController():
	def __init__(self, controller_interface):
		self.controller_interface = controller_interface
		self.up_percent = 0
		self.down_percent = 0
		
	def set_character_display_control_interface(self, character_display_control_interface):
		self.character_display_control_interface = character_display_control_interface
		
	def reset(self):
		self.up_percent = 0
		self.down_percent = 0
		
	def update(self):
		if pyxel.btn(pyxel.KEY_UP):
			self.add_up_control(0.02)
		elif pyxel.btn(pyxel.KEY_DOWN):
			self.add_down_control(0.02)
		elif pyxel.btnp(pyxel.KEY_ENTER):
			self.administer()
			
		self.character_display_control_interface.set_up_control(self.up_percent)
		self.character_display_control_interface.set_down_control(self.down_percent)
			
	def add_up_control(self, percent_increase):
		if self.down_percent == 0:
			self.up_percent += percent_increase
			self.up_percent = min(1, self.up_percent)
		else:
			self.down_percent -= percent_increase
			self.down_percent = max(0, self.down_percent)
		
	def add_down_control(self, percent_increase):
		if self.up_percent == 0:
			self.down_percent += percent_increase
			self.down_percent = min(1, self.down_percent)
		else:
			self.up_percent -= percent_increase
			self.up_percent = max(0, self.up_percent)
			
	def administer(self):
		if self.up_percent > 0:
			up_affector = UpAffector(80, 80 * self.up_percent)
			self.controller_interface.add_affector(up_affector)
			self.up_percent = 0
		if self.down_percent > 0:
			down_affector = DownAffector(400, 1000 * self.down_percent)
			self.controller_interface.add_affector(down_affector)
			self.down_percent = 0

# Affector for the Up control	
class UpAffector(TimeDependentAffector):
	def __init__(self, lifetime, scale):
		super(UpAffector, self).__init__(lifetime)
		self.scale = scale
		
	def f(self, time):
		time = time / self.lifetime
		return self.scale / self.lifetime * (1 - time) * (1 - time)
		
# Affector for the down control
class DownAffector(TimeDependentAffector):
	def __init__(self, lifetime, scale):
		super(DownAffector, self).__init__(lifetime)
		self.scale = scale
		self.remaining_affect_scale = 1 / 2000
		
	def remaining_affect(self):
		t = self.time_elapsed / self.lifetime
		return self.scale * self.remaining_affect_scale * (4 * t*t*t*t*t - 15 * t*t*t*t + 20 * t*t*t - 10 * t*t + 1)
			
	def f(self, time):
		time = time / self.lifetime
		return - self.scale / self.lifetime * time * (1 - time) * (1 - time) * (1 - time)