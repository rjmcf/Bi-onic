import pyxel
from plugins.window import ChildWindow
from bars import FillableBar
from controller import TimeDependentAffector

# The window that shows the character's visible state, and the control UI. Also handles 
# how player input gets translated into Graph affectors.
#TODO Refactor: Should separate these responsibilities, implementation and representation
class CharacterDisplay(ChildWindow):
	def __init__(self, controller_interface):
		super(CharacterDisplay, self).__init__(0,0, 1,0.4) 
		self.background = 2
		self.control_border = 7
		self.up_control = FillableBar(0.9,0.1, 0.05,0.4, True,False, self.background,10, self.control_border)
		self.down_control = FillableBar(0.9,0.5, 0.05,0.4, True,True, self.background,3, self.control_border)
		self.down_reservoir = FillableBar(0.85,0.5, 0.05,0.4, True,False, self.background,3, self.control_border)
		self.child_windows = [self.up_control, self.down_control, self.down_reservoir]
		self.controller_interface = controller_interface
		
	def add_up_control(self, percent_increase):
		if self.down_control.is_empty():
			self.up_control.adjust_bar(percent_increase)
		else:
			self.down_control.adjust_bar(-percent_increase)
		
	def add_down_control(self, percent_increase):
		if self.up_control.is_empty():
			self.down_control.adjust_bar(percent_increase)
		else:
			self.up_control.adjust_bar(-percent_increase)
		
	def administer(self):
		if self.up_control.percent_full > 0:
			up_affector = TimeDependentAffector(0)
			up_percent = self.up_control.percent_full
			up_affector.f = lambda x: -1 * up_percent
			self.controller_interface.add_affector(up_affector)
			self.up_control.percent_full = 0
		if self.down_control.percent_full > 0:
			#TODO Refactor: make the down control follow a curve over time
			down_affector = TimeDependentAffector(0)
			down_percent = self.down_control.percent_full
			down_affector.f = lambda x: 1 * down_percent
			self.controller_interface.add_affector(down_affector)
			self.down_control.percent_full = 0
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.background)
	
# Interface for player to use the controls	
class CharacterControlInterface():
	def __init__(self, character_display):
		self.character_display = character_display
		
	def add_up_control(self, percent_increase):
		self.character_display.add_up_control(percent_increase)
		
	def add_down_control(self, percent_increase):
		self.character_display.add_down_control(percent_increase)
		
	def administer(self):
		self.character_display.administer()