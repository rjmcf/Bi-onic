import pyxel
from root import Root
from character_display import CharacterDisplayControlInterface, CharacterDisplayReservoirInterface, ThreatDisplayInterface
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
		self.line = Line()
		self.controller = Controller(LineInterface(self.line))
		controller_interface = ControllerInterface(self.controller)
		self.player_controller = PlayerController(controller_interface)
		self.environment = Environment(controller_interface, PlayerThreatInterface(self.player_threat), LineStateInterface(self.line))
		self.root_window = Root(self.game_state)
		self.root_window.set_player_threat_display(self.player_threat)
		self.root_window.set_line_display(self.line)
		self.controller.set_character_display_reservoir_interface(CharacterDisplayReservoirInterface(self.root_window.character_display_window))
		self.player_controller.set_character_display_control_interface(CharacterDisplayControlInterface(self.root_window.character_display_window))
		
	def update(self):		
		if self.game_state.game_playing:
			self.player_threat.update()
			self.player_controller.update()
			self.controller.update()
			self.line.update()
			self.environment.update()
			self.root_window.update()
		else:
			if pyxel.btnp(pyxel.KEY_R):
				for thing in [self.game_state, self.player_threat, self.line, self.controller, self.environment, self.root_window]:
					thing.reset()
		
	def start(self):
		pyxel.run(self.update, self.root_window.draw)