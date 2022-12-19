import pyxel
from root import Root
from game_state import GameState
from player_controller import PlayerController
from environment import Environment
from line import Line, LineInterface, LineStateInterface
from controller import Controller, ControllerInterface
from player_threat import PlayerThreat, PlayerThreatInterface
from score_keeper import ScoreKeeper, ScoreKeeperEndGameDelegate
from main_menu import MainMenu
from typing import Any

# Manages the overall functioning of the game. Owns all the components, and makes sure
# they are updated correctly.
# Also owns root window, and makes sure it knows when to draw.
# If a logical component needs a reference to a display element, the convention is to pass
# the logical component to the root window and allow it to set the correct display element.
class Core():
	def __init__(self) -> None:
		# Setup Logical stuff
		self.game_state = GameState()
		self.player_threat = PlayerThreat(self.game_state)
		self.line = Line(self.game_state)
		line_state_interface = LineStateInterface(self.line)
		self.controller = Controller(LineInterface(self.line))
		controller_interface = ControllerInterface(self.controller)
		self.player_controller = PlayerController(controller_interface)
		self.environment = Environment(controller_interface, PlayerThreatInterface(self.player_threat), line_state_interface)
		self.score_keeper = ScoreKeeper(line_state_interface)
		self.game_state.add_kill_player_delegate(ScoreKeeperEndGameDelegate(self.score_keeper))
		self.main_menu = MainMenu(StartGameInterface(self))

		# Setup display stuff
		self.root_window = Root(self.game_state, self.main_menu)
		self.root_window.set_player_threat_display(self.player_threat)
		self.root_window.set_line_display(self.line)
		self.root_window.set_character_display_reservoir_interface(self.controller)
		self.root_window.set_character_display_control_interface(self.player_controller)
		self.root_window.set_character_display_text_interface(self.environment)
		self.root_window.set_score_display(self.score_keeper)

		# State that we start at the Main Menu
		self.root_window.switch_to_main_menu()

	def update(self) -> None:
		if self.game_state.in_game_mode():
			self.update_game_mode()
		elif self.game_state.in_main_menu_mode():
			self.update_main_menu_mode()
		else:
			print("Invalid game mode", self.game_state.game_mode, "detected")
			quit()

	def update_game_mode(self) -> None:
		if self.game_state.is_game_playing():
			if pyxel.btnp(pyxel.KEY_P):
				self.game_state.toggle_paused()

			if not self.game_state.paused:
				self.player_threat.update()
				self.player_controller.update()
				self.controller.update()
				self.line.update()
				self.score_keeper.update()
				self.environment.update()
			# Enable us to show debug even when paused
			self.root_window.update()
		else:
			if pyxel.btnp(pyxel.KEY_R):
				to_be_reset : list[Any] = [
					self.game_state, self.player_threat, self.line, self.controller,
					self.player_controller, self.environment, self.score_keeper,
					self.root_window
				]
				for thing in to_be_reset:
					thing.reset()

	def update_main_menu_mode(self) -> None:
		if pyxel.btnp(pyxel.KEY_UP):
			self.main_menu.move_up()
		elif pyxel.btnp(pyxel.KEY_DOWN):
			self.main_menu.move_down()
		elif pyxel.btnp(pyxel.KEY_RETURN):
			self.main_menu.select()
		# Allow debug windows still
		self.root_window.update()

	def start_game(self) -> None:
		self.game_state.start_game()
		self.root_window.switch_to_game()

	def start(self) -> None:
		pyxel.run(self.update, self.root_window.draw)

# Interface allowing MainMenu to start the game
class StartGameInterface:
	def __init__(self, core : Core) -> None:
		self.core = core

	def start_game(self) -> None:
		self.core.start_game()
