import pyxel
from root import Root
from game_state import GameState
from player_controller import PlayerController
from environment import Environment
from line import Line, LineInterface, LineStateInterface
from controller import Controller, ControllerInterface
from player_threat import PlayerThreat, PlayerThreatInterface

class Core():
	def __init__(self):
		self.game_state = GameState()
		self.player_threat = PlayerThreat(self.game_state)
		self.line = Line(self.game_state)
		self.controller = Controller(LineInterface(self.line))
		controller_interface = ControllerInterface(self.controller)
		self.player_controller = PlayerController(controller_interface)
		self.environment = Environment(controller_interface, PlayerThreatInterface(self.player_threat), LineStateInterface(self.line))
		self.root_window = Root(self.game_state)
		self.root_window.set_player_threat_display(self.player_threat)
		self.root_window.set_line_display(self.line)
		self.root_window.set_character_display_reservoir_interface(self.controller)
		self.root_window.set_character_display_control_interface(self.player_controller)
		self.root_window.set_character_display_text_interface(self.environment)
		
	def update(self):		
		#TODO Unfinished: Stopping line has disastrous effects
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
		
	def start(self):
		pyxel.run(self.update, self.root_window.draw)