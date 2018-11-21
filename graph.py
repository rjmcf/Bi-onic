import pyxel
from plugins.window import ChildWindow
from line import LineDisplay

# Just fills itself with a given colour
#TODO Remove: only needed while we don't have dedicated windows for each section
class TestChild(ChildWindow):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, colour):
		super(TestChild, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.colour = colour
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)

# The window within which the graph is drawn. Keeps track of the Line, and the velocity 
# the line should be moving at
class GraphWindow(ChildWindow):
	def __init__(self):
		super(GraphWindow, self).__init__(0,0.4, 1,0.6)
		self.colour = 6
		self.line_display = LineDisplay(150, -30,10, -100,48, 12, 2)
		self.danger_high = TestChild(0,0, 1,0.4, 9)
		self.danger_low = TestChild(0,0.8, 1,0.2, 8)
		self.child_windows = [self.danger_high, self.danger_low]
		
	def set_line_display(self, line):
		line.set_display(self.line_display)
		
	def update(self):
		super(GraphWindow, self).update()
		
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.colour)
		
	def draw_after_children(self):		
		self.line_display.draw(self.x + self.width//2, self.y + self.height//2)