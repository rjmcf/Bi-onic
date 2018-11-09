import pyxel
from plugins.window import Window, ChildWindow
from palette_settings import PALETTE
from line import Line
from controller import Controller
#from debug import ImageViewer, Tiler, PaletteViewer

RESOURCE = "assets/bionic_resources1.pyxel"
		
class Root(Window):
	def __init__(self, width, height, caption):
		super(Root, self).__init__(0,0, width, height)
		self.caption = caption
		self.palette = PALETTE
		character_display_window = TestChild(0,0, 1,0.4, 3)
		control_bars = TestChild(0.9,0.1, 0.05,0.8, 14)
		character_display_window.child_windows = [control_bars]
		graph_area = GraphWindow(0,0.4, 1,0.6, 6)  #TestChild(0,0.4, 1,0.6, 12)
		#danger_high = TestChild(0,0, 1,0.5, 9)
		#danger_low = TestChild(0,0.8, 1,0.2, 8)
		#graph_area.child_windows = [danger_high, danger_low]
		self.controller = Controller(graph_area)
		self.child_windows = self.reserve_children = [character_display_window, graph_area]
		self.debug_windows = []#ImageViewer(self.palette), Tiler(), PaletteViewer()]
		pyxel.init(self.width, self.height, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		
	def start(self):
		pyxel.run(self.update, self.draw)
		
	def update(self):
		super(Root, self).update()
		
		self.controller.update()
		
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
		
class GraphWindow(ChildWindow):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, colour):
		super(GraphWindow, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.colour = colour
		self.line = Line(150, 12, 2)
		self.velocity = 0
		
	def update(self):
		super(GraphWindow, self).update()
		
		if pyxel.btnp(pyxel.KEY_ENTER):
			self.line.toggle_started()
			
		self.line.update(self.velocity)
		
	def add_velocity(self, velocity_adjustment):
		self.velocity += velocity_adjustment
		
	def draw_child(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)
		# Draw danger zones
		
		self.line.draw(self.x + self.width//2, self.y + self.height//2)
		