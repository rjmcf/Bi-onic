from plugins.window import Window
from plugins.sprite import TextSprite, Anchor
from plugins.geometry import Proportion2D
from plugins.delegate import Delegate
from line import LineState

class ScoreKeeper():
	def __init__(self, line_state_interface):
		self.score = 0
		self.frames_for_increase = 10
		self.frames_for_increase_in_danger = 30
		self.score_increase = 10
		self.current_frame = 0
		self.line_state_interface = line_state_interface
		self.high_score = 0
		
	def reset(self):
		self.score = 0
		self.current_frame = 0
		
	def set_display(self, display):
		self.display = display
		
	def increase_score(self, amount):
		self.score += amount
		self.display.update_text_for_score(self.score)
		
	def on_game_ended(self):
		if self.score > self.high_score:
			self.high_score = self.score
		self.display.on_game_ended(self.high_score)
		
	def update(self):
		self.current_frame += 1
		
		if self.line_state_interface.get_current_line_state() == LineState.STATE_NORMAL:
			if not self.current_frame % self.frames_for_increase:
				self.increase_score(self.score_increase)
		else:
			if not self.current_frame % self.frames_for_increase_in_danger:
				self.increase_score(self.score_increase)
				
class ScoreKeeperEndGameDelegate(Delegate):
	def __init__(self, score_keeper):
		self.score_keeper = score_keeper
		
	def execute(self, *args, **kwargs):
		self.score_keeper.on_game_ended()
				
class ScoreDisplayWindow(Window):
	def __init__(self):	
		super(ScoreDisplayWindow, self).__init__(Proportion2D(0,0), Proportion2D(1,1))
		self.num_zeros = 5
		self.update_text_for_score(0)
		self.game_ended = False
		
	def reset(self):
		self.game_ended = False
		
	def on_game_ended(self, high_score):
		self.high_score_text = TextSprite("High Score: " + str(high_score).zfill(self.num_zeros), 7)
		self.game_ended = True
		
	def update_text_for_score(self, score):
		self.score_text = TextSprite("Score: " + str(score).zfill(self.num_zeros), 7)
		
	def draw_before_children(self):
		self.score_text.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0))), Anchor.MIDDLE)
		if self.game_ended:
			self.high_score_text.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.1))), Anchor.MIDDLE)
		
	
		