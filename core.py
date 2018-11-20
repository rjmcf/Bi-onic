import pyxel
from root import Root
from character_display import CharacterDisplayControlInterface, CharacterDisplayReservoirInterface, ThreatDisplayInterface
from game_state import GameState, ThreatInterface
from player_controller import PlayerController
from environment import Environment
from graph import LineStateInterface
from controller import Controller, ControllerInterface

class Core():
	def __init__(self):
		self.game_state = GameState()
		threat_interface = ThreatInterface(self.game_state)
		self.controller = Controller()
		controller_interface = ControllerInterface(self.controller)
		self.player_controller = PlayerController(controller_interface)
		self.environment = Environment(controller_interface, threat_interface)
		self.root_window = Root(self.game_state)
		threat_display_interface = ThreatDisplayInterface(self.root_window.character_display_window)
		self.game_state.set_threat_display_interface(threat_display_interface)
		line_state_interface = LineStateInterface(self.root_window.graph_area)
		character_display_reservoir_interface = CharacterDisplayReservoirInterface(self.root_window.character_display_window)
		character_display_control_interface = CharacterDisplayControlInterface(self.root_window.character_display_window)
		self.controller.set_graph(self.root_window.graph_area)
		self.controller.set_character_display_reservoir_interface(character_display_reservoir_interface)
		self.player_controller.set_character_display_control_interface(character_display_control_interface)
		self.environment.set_line_state_interface(line_state_interface)
		
	def update(self):		
		if self.game_state.game_playing:
			self.root_window.update()
			self.player_controller.update()
			self.controller.update()
			self.environment.update()
			self.game_state.update()
		else:
			if pyxel.btnp(pyxel.KEY_R):
				for thing in [self.game_state, self.controller, self.environment, self.root_window]:
					thing.reset()
		
	def start(self):
		pyxel.run(self.update, self.root_window.draw)