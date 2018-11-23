import pyxel
from plugins.window import Window
from plugins.geometry import Proportion2D
from line import LineDisplay

# Just fills itself with a given colour
#TODO Remove: only needed while we don't have dedicated windows for each section
class TestChild(Window):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, colour):
		super(TestChild, self).__init__(Proportion2D(x_prop, y_prop), Proportion2D(width_prop, height_prop))
		self.colour = colour
		
	def draw_before_children(self):
		pyxel.rect(*self.corner, *self.corner.br_of(self.size), self.colour)

# The window within which the graph is drawn. Keeps track of the Line, and the velocity 
# the line should be moving at
class GraphWindow(Window):
	def __init__(self, parent_corner, parent_size):
		super(GraphWindow, self).__init__(Proportion2D(0,0.4), Proportion2D(1,0.6), parent_corner, parent_size)
		self.colour = 6
		self.start_prop = Proportion2D(1/2, 1/2)
		self.high_region_prop = 2/5
		self.low_region_prop = 1/5
		self.line_display = LineDisplay(150, 
										-(1-self.start_prop.y-self.low_region_prop)*self.size.y,
										(self.start_prop.y-self.high_region_prop)*self.size.y, 
										(self.start_prop.y-1)*self.size.y,
										self.start_prop.y*self.size.y, 
										12, 2)
		self.danger_high = TestChild(0,0, 1,self.high_region_prop, 9)
		self.danger_low = TestChild(0,1-self.low_region_prop, 1,self.low_region_prop, 8)
		self.child_windows = [self.danger_high, self.danger_low]
		
	def set_line_display(self, line):
		line.set_display(self.line_display)
		
	def update(self):
		super(GraphWindow, self).update()
		
		
	def draw_before_children(self):
		pyxel.rect(*self.corner, *self.corner.br_of(self.size), self.colour)
		
	def draw_after_children(self):
		self.line_display.draw(self.corner.br_of(self.size.scale(self.start_prop)))