import pyxel
from plugins.window import ChildWindow
from bars import FillableBar

# The window that shows the character's visible state, and the control UI. 
class CharacterDisplay(ChildWindow):
	def __init__(self):
		super(CharacterDisplay, self).__init__(0,0, 1,0.4) 
		self.background = 2
		self.control_border = 7
		self.up_control = FillableBar(0.9,0.1, 0.05,0.4, True,False, self.background,10, self.control_border)
		self.down_control = FillableBar(0.9,0.5, 0.05,0.4, True,True, self.background,3, self.control_border)
		self.down_reservoir = FillableBar(0.85,0.5, 0.05,0.4, True,False, self.background,3, self.control_border)
		self.child_windows = [self.up_control, self.down_control, self.down_reservoir]
		
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
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.background)		
	
# Interface for player to use the controls	
class CharacterDisplayControlInterface():
	def __init__(self, character_display):
		self.character_display = character_display
		
	def add_up_control(self, percent_increase):
		self.character_display.add_up_control(percent_increase)
		
	def get_up_percent_full(self):
		return self.character_display.up_control.percent_full
		
	def empty_up(self):
		self.character_display.up_control.percent_full = 0
		
	def add_down_control(self, percent_increase):
		self.character_display.add_down_control(percent_increase)
		
	def get_down_percent_full(self):
		return self.character_display.down_control.percent_full
		
	def empty_down(self):
		self.character_display.down_control.percent_full = 0
		