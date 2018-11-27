class GameMode():
	MAIN_MENU = 0
	GAME = 1

class GameState():
	def __init__(self):
		self.game_playing = True
		self.paused = True
		self.game_mode = GameMode.MAIN_MENU
		
	def start_game(self):
		self.game_mode = GameMode.GAME
		
	def exit_to_menu(self):
		self.game_mode = GameMode.MAIN_MENU
		
	def in_game_mode(self):
		return self.game_mode == GameMode.GAME
		
	def in_main_menu_mode(self):
		return self.game_mode == GameMode.MAIN_MENU
		
	def toggle_paused(self):
		self.paused = not self.paused
		
	def reset(self):
		self.game_playing = True
		self.paused = True
		
