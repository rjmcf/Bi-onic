from plugins.delegate import Delegate
from plugins.enum import Enum

# Represents Game Modes that the game can be in
class GameMode(Enum):
	MAIN_MENU = 0
	GAME = 1

# Records the current state of the game including:
#	Our current mode
#	Whether the player is alive
#	Whether the game is paused
class GameState():
	def __init__(self) -> None:
		self.game_playing = True
		self.paused = False
		self.game_mode = GameMode(GameMode.MAIN_MENU)
		self.kill_player_delegates : list[Delegate] = []

	def start_game(self) -> None:
		self.game_mode = GameMode(GameMode.GAME)

	def kill_player(self) -> None:
		if self.game_playing:
			self.game_playing = False
			for delegate in self.kill_player_delegates:
				delegate.execute()

	def add_kill_player_delegate(self, delegate : Delegate) -> None:
		self.kill_player_delegates.append(delegate)

	def is_game_playing(self) -> bool:
		return self.game_playing

	def exit_to_menu(self) -> None:
		self.game_mode = GameMode(GameMode.MAIN_MENU)

	def in_game_mode(self) -> bool:
		return self.game_mode == GameMode.GAME

	def in_main_menu_mode(self) -> bool:
		return self.game_mode == GameMode.MAIN_MENU

	def toggle_paused(self) -> None:
		self.paused = not self.paused

	def reset(self) -> None:
		self.game_playing = True
		self.paused = False
