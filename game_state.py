class GameState():
	def __init__(self):
		self.game_playing = True
		self.paused = True
		
	def toggle_paused(self):
		self.paused = not self.paused
		
	def reset(self):
		self.game_playing = True
		self.paused = True
		
