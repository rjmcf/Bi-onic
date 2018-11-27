import pyxel
from root import Root
from game_state import GameState
from player_controller import PlayerController
from environment import Environment
from line import Line, LineInterface, LineStateInterface
from controller import Controller, ControllerInterface
from player_threat import PlayerThreat, PlayerThreatInterface
from main_menu import MainMenu

class Core():
	def __init__(self):
		self.game_state = GameState()
		self.player_threat = PlayerThreat(self.game_state)
		self.line = Line(self.game_state)
		self.controller = Controller(LineInterface(self.line))
		controller_interface = ControllerInterface(self.controller)
		self.player_controller = PlayerController(controller_interface)
		self.environment = Environment(controller_interface, PlayerThreatInterface(self.player_threat), LineStateInterface(self.line))
		self.main_menu = MainMenu(StartGameInterface(self))
		self.root_window = Root(self.game_state, self.main_menu)
		self.root_window.set_player_threat_display(self.player_threat)
		self.root_window.set_line_display(self.line)
		self.root_window.set_character_display_reservoir_interface(self.controller)
		self.root_window.set_character_display_control_interface(self.player_controller)
		self.root_window.set_character_display_text_interface(self.environment)
		self.root_window.set_main_menu_display(self.main_menu)
		
		self.root_window.switch_to_main_menu()
		
	def update(self):		
		if self.game_state.in_game_mode():	
			self.update_game_mode()
		elif self.game_state.in_main_menu_mode():
			self.update_main_menu_mode()
		else:
			print("Invalid game mode", self.game_state.game_mode, "detected")
			quit() 
						
	def update_game_mode(self):
		if self.game_state.game_playing:
			if pyxel.btnp(pyxel.KEY_P):
				self.game_state.toggle_paused()
				
			if not self.game_state.paused:
				self.player_threat.update()
				self.player_controller.update()
				self.controller.update()
				self.line.update()
				self.environment.update()
			self.root_window.update()
		else:
			if pyxel.btnp(pyxel.KEY_R):
				to_be_reset = [
					self.game_state, self.player_threat, self.line, self.controller, 
					self.player_controller, self.environment, self.root_window
				]
				for thing in to_be_reset:
					thing.reset()
	
	def update_main_menu_mode(self):
		if pyxel.btnp(pyxel.KEY_UP):
			self.main_menu.move_up()
		elif pyxel.btnp(pyxel.KEY_DOWN):
			self.main_menu.move_down()
		elif pyxel.btnp(pyxel.KEY_ENTER):
			self.main_menu.select()
			
	def start_game(self):
		self.game_state.start_game()
		self.root_window.switch_to_game()
		
	def start(self):
		pyxel.run(self.update, self.root_window.draw)
		
class StartGameInterface:
	def __init__(self, core):
		self.core = core
		
	def start_game(self):
		self.core.start_game()