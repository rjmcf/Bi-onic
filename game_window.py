import pyxel
from plugins.window import Window, ChildWindow
from palette_settings import PALETTE
from line import Line, LineState
from controller import Controller, TimeDependentAffector
from resource_settings import RESOURCE
from debug import ImageViewer, Tiler, PaletteViewer

		
class Root(Window):
	def __init__(self, width, height, caption):
		super(Root, self).__init__(0,0, width, height)
		self.caption = caption
		self.palette = PALETTE
		pyxel.init(self.width, self.height, caption=self.caption, palette=self.palette.get_palette())
		pyxel.load(RESOURCE)
		character_display_window = TestChild(0,0, 1,0.4, 3)
		control_bars = FillableBar(0.9,0.1, 0.05,0.8, True, False, 3,14, 0)
		character_display_window.child_windows = [control_bars]
		graph_area = GraphWindow(0,0.4, 1,0.6, 6)
		danger_high = TestChild(0,0, 1,0.4, 9)
		danger_low = TestChild(0,0.8, 1,0.2, 8)
		graph_area.child_windows = [danger_high, danger_low]
		self.controller = Controller(graph_area)
		self.child_windows = self.reserve_children = [character_display_window, graph_area]
		self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer()]
		
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
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)
		
class GraphWindow(ChildWindow):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, colour):
		super(GraphWindow, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.colour = colour
		self.line_state = LineState()
		self.line = Line(150, -30,10, 0,0, self.line_state, 12, 2)
		self.velocity = 0
		
	def update(self):
		super(GraphWindow, self).update()
		
		if pyxel.btnp(pyxel.KEY_ENTER):
			self.line.toggle_started()
			
		self.line.update(self.velocity)
		
	def add_velocity(self, velocity_adjustment):
		self.velocity += velocity_adjustment
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)
		
	def draw_after_children(self):
		if self.line_state.state == LineState.STATE_OFF:
			self.colour = 0
		elif self.line_state.state == LineState.STATE_NORMAL:
			self.colour = 1
		elif self.line_state.state == LineState.STATE_HIGH:
			self.colour = 9
		elif self.line_state.state == LineState.STATE_LOW:
			self.colour = 8
		else:
			raise ValueError()
		
		self.line.draw(self.x + self.width//2, self.y + self.height//2)
		
class FillableBar(ChildWindow):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, is_vertical, fill_positive, back_colour, fill_colour, border_colour = None):
		super(FillableBar, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.percent_full = 0
		self.is_vertical = is_vertical
		self.fill_positive = fill_positive
		self.back_colour = back_colour
		self.fill_colour = fill_colour
		self.border_colour = border_colour
		
	def adjust_bar(self, percent_difference):
		self.percent_full += percent_difference
		self.percent_full = min(self.percent_full, 1)
		self.percent_full = max(0, self.percent_full)
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.back_colour)
		if self.is_vertical:
			top_left_x = self.x
			top_left_y = self.y if self.fill_positive else self.y + (1-self.percent_full) * self.height
			bottom_right_x = self.x + self.width
			bottom_right_y = self.y + self.percent_full * self.height if self.fill_positive else self.y + self.height
		else:
			top_left_x = self.x if self.fill_positive else self.x + (1-self.percent_full) * self.width
			top_left_y = self.y 
			bottom_right_x = self.x + self.percent_full * self.width if self.fill_positive else self.x + self.width
			bottom_right_y = self.y + self.height
		pyxel.rect(top_left_x, top_left_y, bottom_right_x, bottom_right_y, self.fill_colour)
		
		if self.border_colour != None:
			pyxel.rectb(self.x, self.y, self.x + self.width, self.y + self.height, self.border_colour)
		