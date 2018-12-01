# Represents Game Modes that the game can be in
class GameMode():
	MAIN_MENU = 0
	GAME = 1

# Records the current state of the game including:
#	Our current mode
#	Whether the player is alive
#	Whether the game is paused
class GameState():
	def __init__(self):
		self.game_playing = True
		self.paused = False
		self.game_mode = GameMode.MAIN_MENU
		self.kill_player_delegates = []
		
	def start_game(self):
		self.game_mode = GameMode.GAME
		
	def kill_player(self):
		if self.game_playing:
			self.game_playing = False
			for delegate in self.kill_player_delegates:
				delegate.execute()
				
	def add_kill_player_delegate(self, delegate):
		self.kill_player_delegates.append(delegate)
		
	def is_game_playing(self):
		return self.game_playing
		
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
		self.paused = False
		
