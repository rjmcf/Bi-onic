import pyxel
from controller import TimeDependentAffector

# Used by the Player to have an effect on the graph, via the ControlInterface.
class PlayerController():
	def __init__(self, character_display_control_interface, controller_interface):
		self.character_display_control_interface = character_display_control_interface
		self.controller_interface = controller_interface
		
	def update(self):
		if pyxel.btn(pyxel.KEY_UP):
			self.character_display_control_interface.add_up_control(0.02)
		elif pyxel.btn(pyxel.KEY_DOWN):
			self.character_display_control_interface.add_down_control(0.02)
		elif pyxel.btnp(pyxel.KEY_ENTER):
			self.administer()
			
	def administer(self):
		up_percent = self.character_display_control_interface.get_up_percent_full()
		down_percent = self.character_display_control_interface.get_down_percent_full()
		if up_percent > 0:
			up_affector = UpAffector(80, 80 * up_percent)
			self.controller_interface.add_affector(up_affector)
			self.character_display_control_interface.empty_up()
		if down_percent > 0:
			down_affector = DownAffector(400, 1000 * down_percent)
			self.controller_interface.add_affector(down_affector)
			self.character_display_control_interface.empty_down()
			
class UpAffector(TimeDependentAffector):
	def __init__(self, lifetime, scale):
		super(UpAffector, self).__init__(lifetime)
		self.scale = scale
		
	def f(self, time):
		time = time / self.lifetime
		return self.scale / self.lifetime * (1 - time) * (1 - time)
		
class DownAffector(TimeDependentAffector):
	def __init__(self, lifetime, scale):
		super(DownAffector, self).__init__(lifetime)
		self.scale = scale
		
	def f(self, time):
		time = time / self.lifetime
		return - self.scale / self.lifetime * time * (1 - time) * (1 - time) * (1 - time)