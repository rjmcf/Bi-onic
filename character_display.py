import pyxel
from plugins.window import ChildWindow
from bars import FillableBar

class CharacterDisplay(ChildWindow):
	def __init__(self):
		super(CharacterDisplay, self).__init__(0,0, 1,0.4) 
		self.control_bars = FillableBar(0.9,0.1, 0.05,0.8, True, False, 3,14, 0)
		self.child_windows = [self.control_bars] 
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, 3)