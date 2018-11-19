import pyxel
from plugins.window import ChildWindow
from line import Line, LineState

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
		self.line_state = LineState()
		self.line = Line(150, -30,10, 0,0, self.line_state, 12, 2)
		self.velocity = 0
		self.danger_high = TestChild(0,0, 1,0.4, 9)
		self.danger_low = TestChild(0,0.8, 1,0.2, 8)
		self.child_windows = [self.danger_high, self.danger_low]
		
	def reset(self):
		self.line.reset()
		
	def update(self):
		super(GraphWindow, self).update()
		
		if pyxel.btnp(pyxel.KEY_SPACE):
			self.line.toggle_started()
			
		self.line.update(self.velocity)
		self.velocity = 0
		
	# method called to affect the line's velocity, whether by player or environment
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
		
class LineStateInterface():
	def __init__(self, graph_window):
		self.graph_window = graph_window
		
	def get_current_line_state(self):
		return self.graph_window.line_state.state