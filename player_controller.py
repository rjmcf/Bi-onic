import pyxel
from character_display import CharacterControlInterface

# Used by the Player to have an effect on the graph, via the CharacterController
class PlayerController():
	def __init__(self, character_control_interface):
		self.character_control_interface = character_control_interface
		
	def update(self):
		if pyxel.btn(pyxel.KEY_UP):
			self.character_control_interface.add_up_control(0.02)
		elif pyxel.btn(pyxel.KEY_DOWN):
			self.character_control_interface.add_down_control(0.02)
		elif pyxel.btnp(pyxel.KEY_ENTER):
			self.character_control_interface.administer()