import pyxel
from plugins.window import Window
from line import LineDisplay

# Just fills itself with a given colour
#TODO Remove: only needed while we don't have dedicated windows for each section
class TestChild(Window):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, colour):
		super(TestChild, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.colour = colour
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)

# The window within which the graph is drawn. Keeps track of the Line, and the velocity 
# the line should be moving at
class GraphWindow(Window):
	def __init__(self, parent_x,parent_y, parent_width,parent_height):
		super(GraphWindow, self).__init__(0,0.4, 1,0.6, parent_x,parent_y, parent_width,parent_height)
		self.colour = 6
		self.start_x_prop = 1/2
		self.start_y_prop = 1/2
		self.high_region_prop = 2/5
		self.low_region_prop = 1/5
		self.line_display = LineDisplay(150, 
										-(1-self.start_y_prop-self.low_region_prop)*self.height,
										(self.start_y_prop-self.high_region_prop)*self.height, 
										(self.start_y_prop-1)*self.height,
										self.start_y_prop*self.height, 
										12, 2)
		self.danger_high = TestChild(0,0, 1,self.high_region_prop, 9)
		self.danger_low = TestChild(0,1-self.low_region_prop, 1,self.low_region_prop, 8)
		self.child_windows = [self.danger_high, self.danger_low]
		
	def set_line_display(self, line):
		line.set_display(self.line_display)
		
	def update(self):
		super(GraphWindow, self).update()
		
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)
		
	def draw_after_children(self):
		self.line_display.draw(self.x + self.start_x_prop*self.width, self.y + self.start_y_prop*self.height)