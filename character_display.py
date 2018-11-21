import pyxel
from plugins.window import ChildWindow
from bars import FillableBar
from player_controller import DownAffector
from player_threat import PlayerThreatWindow

# The window that shows the character's visible state, and the control UI. 
class CharacterDisplay(ChildWindow):
	def __init__(self):
		super(CharacterDisplay, self).__init__(0,0, 1,0.4) 
		self.background = 2
		self.control_border = 7
		self.up_control = FillableBar(0.9,0.1, 0.05,0.4, True,False, self.background,10, self.control_border)
		self.down_control = FillableBar(0.9,0.5, 0.05,0.4, True,True, self.background,3, self.control_border)
		self.down_reservoir = FillableBar(0.85,0.5, 0.05,0.4, True,False, self.background,3, self.control_border)
		self.player_threat_display = PlayerThreatWindow(0.05,0.1, 0.05,0.8, self.background, self.control_border)
		self.child_windows = [self.up_control, self.down_control, self.down_reservoir, self.player_threat_display]
		
	def set_character_display_reservoir_interface(self, controller):
		controller.set_character_display_reservoir_interface(CharacterDisplayReservoirInterface(self))
		
	def set_character_display_control_interface(self, player_controller):
		player_controller.set_character_display_control_interface(CharacterDisplayControlInterface(self))
		
	def reset(self):
		self.up_control.set_bar(0)
		self.down_control.set_bar(0)
		self.down_reservoir.set_bar(0)
			
	def empty_down_reservoir(self):
		self.down_reservoir.set_bar(0)
		
	def add_down_reservoir_amount(self, percent_increase):
		self.down_reservoir.adjust_bar(percent_increase)
		
	def set_player_threat_display(self, player_threat):
		player_threat.set_display(self.player_threat_display)
			
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.background)		
	
# Interface for player to use the controls	
class CharacterDisplayControlInterface():
	def __init__(self, character_display):
		self.character_display = character_display
		
	def set_up_control(self, percent):
		self.character_display.up_control.set_bar(percent)
		
	def set_down_control(self, percent):
		self.character_display.down_control.set_bar(percent)
		
# Interface for controller to use the reservoir UI
class CharacterDisplayReservoirInterface():
	def __init__(self, character_display):
		self.character_display = character_display
		
	def empty_down_reservoir(self):
		self.character_display.empty_down_reservoir()
		
	def add_down_reservoir_amount(self, affector):
		if (isinstance(affector, DownAffector)):
			ticks_left = affector.lifetime + 1 - affector.time_elapsed
			self.character_display.add_down_reservoir_amount(ticks_left / 1000)
			
class ThreatDisplayInterface():
	def __init__(self, character_display):
		self.character_display = character_display
		
	def set_threat_percentage(self, threat_percentage):
		self.character_display.set_threat_percentage(threat_percentage)
		