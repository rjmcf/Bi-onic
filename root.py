import pyxel
from plugins.window import Window, ChildWindow
from palette_settings import PALETTE
from line import Line
from graph import GraphWindow
from character_display import CharacterDisplay
from resource_settings import RESOURCE
from debug import ImageViewer, Tiler, PaletteViewer

# Determines whether we will allow DEBUG screens to be shown
DEBUG = True
	
# Currently owns the game as a whole, which boils down to setting up the layout and making
# sure all the components have the data they require
#TODO Refactor: separate out some responsibilities.
class Root(Window):
	def __init__(self, game_state):
		super(Root, self).__init__(0,0, 255,160)
		self.caption = "Bi-onic"
		self.palette = PALETTE
		self.game_state = game_state
		# This line needs to come before any Pyxel imports are used, otherwise they can't 
		# be imported
		pyxel.init(self.width, self.height, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		self.character_display_window = CharacterDisplay()
		self.graph_area = GraphWindow()
		# Keep two copies of game windows, so we can switch away and back to them
		self.child_windows = self.reserve_children = [self.character_display_window, self.graph_area]
		if DEBUG:
			self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer()]
				
	def toggle_window(self, window):
		if window in self.child_windows:
			self.child_windows = self.reserve_children
		else:
			self.child_windows = [window]
			
	def reset(self):
		for thing in [self.graph_area, self.character_display_window]:
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
			pyxel.text(0,0, "Press R to Restart", 7)
		
		