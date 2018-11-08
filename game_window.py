import pyxel
from plugins.window import Window, ChildWindow
from palette_settings import PALETTE
from debug import ImageViewer, Tiler, PaletteViewer

RESOURCE = "assets/bionic_resources1.pyxel"
		
class Root(Window):
	def __init__(self, width, height, caption, child_windows):
		super(Root, self).__init__(0,0, width, height)
		self.caption = caption
		self.palette = PALETTE
		pyxel.init(self.width, self.height, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer()]
		self.child_windows = self.reserve_children = child_windows
		
	def start(self):
		pyxel.run(self.update, self.draw)
		
	def update(self):
		super(Root, self).update()
		
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
			
			
class TestChild(ChildWindow):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, colour):
		super(TestChild, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.colour = colour
		
	def draw_child(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)