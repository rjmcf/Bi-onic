import pyxel
from plugins.window import Window, ChildWindow
from palette_settings import PALETTE
from line import Line
from controller import Controller
from graph import GraphWindow
from character_display import CharacterDisplay
from resource_settings import RESOURCE
from debug import ImageViewer, Tiler, PaletteViewer

DEBUG = True
	
class Root(Window):
	def __init__(self, width, height, caption):
		super(Root, self).__init__(0,0, width, height)
		self.caption = caption
		self.palette = PALETTE
		pyxel.init(self.width, self.height, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		character_display_window = CharacterDisplay()
		graph_area = GraphWindow()
		self.controller = Controller(graph_area)
		self.child_windows = self.reserve_children = [character_display_window, graph_area]
		if DEBUG:
			self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer()]
		
	def start(self):
		pyxel.run(self.update, self.draw)
		
	def update(self):
		super(Root, self).update()
		
		self.controller.update()
		
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
		
		