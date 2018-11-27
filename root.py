import pyxel
from plugins.window import TopLevelWindow, Window
from plugins.geometry import Size, Point
from plugins.sprite import TextSprite
from palette_settings import PALETTE
from graph import GraphWindow
from character_display import CharacterDisplay
from resource_settings import RESOURCE
from debug import ImageViewer, Tiler, PaletteViewer, GraphImager, TextImager

# Determines whether we will allow DEBUG screens to be shown
DEBUG = True
	
# Currently owns the game as a whole, which boils down to setting up the layout and making
# sure all the components have the data they require
#TODO Refactor: separate out some responsibilities.
class Root(TopLevelWindow):
	def __init__(self, game_state):
		super(Root, self).__init__(Size(255,160))
		self.caption = "Bi-onic"
		self.palette = PALETTE
		self.game_state = game_state
		# This line needs to come before any Pyxel imports are used, otherwise they can't 
		# be imported
		pyxel.init(*self.size, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		self.character_display_window = CharacterDisplay()
		self.graph_area = GraphWindow(Point(0,0), self.size)
		# Keep two copies of game windows, so we can switch away and back to them
		self.windows = self.reserve_children = [self.character_display_window, self.graph_area]
		if DEBUG:
			self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer(), GraphImager(), TextImager()]
			if len(self.debug_windows) != len(set(self.debug_windows)):
				print("Duplicate debug window keys found!")
				quit()
			
		#TODO Remove: Testing only
		self.restart_text = TextSprite("Press R to Restart", 7)
				
	def toggle_window(self, window):
		if window in self.windows:
			self.windows = self.reserve_children
		else:
			self.windows = [window]
			
	def set_player_threat_display(self, player_threat):
		self.character_display_window.set_player_threat_display(player_threat)
		
	def set_line_display(self, line):
		self.graph_area.set_line_display(line)
		
	def set_character_display_reservoir_interface(self, controller):
		self.character_display_window.set_character_display_reservoir_interface(controller)
		
	def set_character_display_control_interface(self, player_controller):
		self.character_display_window.set_character_display_control_interface(player_controller)
		
	def set_character_display_text_interface(self, environment):
		self.character_display_window.set_character_display_text_interface(environment)
			
	def reset(self):
		for thing in [self.character_display_window]:
			thing.reset()
			
	def update(self):
		super(Root, self).update()
		if DEBUG:
			for debug_window in self.debug_windows:
				if pyxel.btnp(debug_window.toggle_key):
					self.toggle_window(debug_window)		
			
	def draw(self):
		pyxel.cls(0)
		super(Root, self).draw()
		
		if not self.game_state.game_playing:
			self.restart_text.draw(Point(self.size.x//2,0), True)
		
		