from plugins.window import Window
from plugins.sprite import TextSprite, Anchor
from plugins.geometry import Proportion2D
from line import LineState

class ScoreKeeper():
	def __init__(self, line_state_interface):
		self.score = 0
		self.frames_for_increase = 10
		self.frames_for_increase_in_danger = 30
		self.score_increase = 10
		self.current_frame = 0
		self.line_state_interface = line_state_interface
		
	def reset(self):
		self.score = 0
		self.current_frame = 0
		
	def set_display(self, display):
		self.display = display
		
	def increase_score(self, amount):
		self.score += amount
		self.display.update_text_for_score(self.score)
		
	def update(self):
		self.current_frame += 1
		
		if self.line_state_interface.get_current_line_state() == LineState.STATE_NORMAL:
			if not self.current_frame % self.frames_for_increase:
				self.increase_score(self.score_increase)
		else:
			if not self.current_frame % self.frames_for_increase_in_danger:
				self.increase_score(self.score_increase)
				
				
class ScoreDisplayWindow(Window):
	def __init__(self):	
		super(ScoreDisplayWindow, self).__init__(Proportion2D(0,0), Proportion2D(1,1))
		self.update_text_for_score(0)
		
	def update_text_for_score(self, score):
		self.score_text = TextSprite("Score: " + str(score).zfill(5), 7)
		
	def draw_before_children(self):
		self.score_text.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0))), Anchor.MIDDLE)
		
	
		