import pyxel
from plugins.window import Window, ChildWindow
from palette_settings import PALETTE
from line import Line
from controller import Controller, ControllerInterface
from graph import GraphWindow, LineStateInterface
from character_display import CharacterDisplay, CharacterDisplayControlInterface, CharacterDisplayReservoirInterface, ThreatDisplayInterface
from player_controller import PlayerController
from environment import Environment
from resource_settings import RESOURCE
from game_state import GameState, ThreatInterface
from debug import ImageViewer, Tiler, PaletteViewer

# Determines whether we will allow DEBUG screens to be shown
DEBUG = True
	
# Currently owns the game as a whole, which boils down to setting up the layout and making
# sure all the components have the data they require
#TODO Refactor: separate out some responsibilities.
class Root(Window):
	def __init__(self, width, height, caption):
		super(Root, self).__init__(0,0, width, height)
		self.caption = caption
		self.palette = PALETTE
		# This line needs to come before any Pyxel imports are used, otherwise they can't 
		# be imported
		pyxel.init(self.width, self.height, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		character_display_window = CharacterDisplay()
		character_display_control_interface = CharacterDisplayControlInterface(character_display_window)
		character_display_reservoir_interface = CharacterDisplayReservoirInterface(character_display_window)
		threat_display_interface = ThreatDisplayInterface(character_display_window)
		self.game_state = GameState(threat_display_interface)
		threat_interface = ThreatInterface(self.game_state)
		graph_area = GraphWindow()
		line_state_interface = LineStateInterface(graph_area)
		self.controller = Controller(graph_area, character_display_reservoir_interface)
		controller_interface = ControllerInterface(self.controller)
		self.player_controller = PlayerController(character_display_control_interface, controller_interface)
		self.environment = Environment(controller_interface, line_state_interface, threat_interface)
		# Keep two copies of game windows, so we can switch away and back to them
		self.child_windows = self.reserve_children = [character_display_window, graph_area]
		if DEBUG:
			self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer()]
		
	def start(self):
		pyxel.run(self.update, self.draw)
		
	def update(self):
		super(Root, self).update()
		
		self.player_controller.update()
		self.controller.update()
		self.environment.update()
		self.game_state.update()
		
		if DEBUG:
			for debug_window in self.debug_windows:
				if pyxel.btnp(debug_window.toggle_key):
					self.toggle_window(debug_window)
				
	def toggle_window(self, window):
		if window in self.child_windows:
			self.child_windows = self.reserve_children
		else:
			self.child_windows = [window]
			
	def draw(self):
		pyxel.cls(0)
		super(Root, self).draw()
		
		