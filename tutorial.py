import pyxel
from plugins.window import Window
from plugins.geometry import Point, Size, Proportion2D
from plugins.sprite import TextSprite, Anchor

class Tutorial():
	def __init__(self, start_game_interface):
		self.start_game_interface = start_game_interface
		self.frames_past = 0
		
	def reset(self):
		self.frames_past = 0
		
	def set_display(self, display):	
		self.display = display
		
	def update(self):
		self.frames_past += 1
		
		if pyxel.btnp(pyxel.KEY_ENTER):
			self.start_game_interface.start_game()
	
	def start(self):
		pass
		
		
class TutorialWindow(Window):
	def __init__(self):
		super(TutorialWindow, self).__init__(Point(0,0), Size(1,1))
		self.title_text = TextSprite("Tutorial", 7)
		
	def draw_before_children(self):
		self.title_text.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.2))), Anchor.MIDDLE)