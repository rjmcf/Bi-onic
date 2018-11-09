import pyxel

class Line():
	def __init__(self, length, low_border, high_border, low_bound, high_bound, line_state, color, width = 0):
		self.length = length
		self.low_border = low_border
		self.high_border = high_border
		self.low_bound = low_bound
		self.high_bound = high_bound
		self.line_state = line_state
		self.color = color
		self.width = width
		self.current_height = 0
		self.segments = [self.current_height]
		self.started = False
		
	def toggle_started(self):	
		self.started = not self.started
		
	def update(self, adjustment):
		if not self.started:
			self.line_state.state = LineState.STATE_OFF
			return
			
		self.current_height += adjustment
		
		if self.current_height > self.high_border:
			self.line_state.state = LineState.STATE_HIGH
		elif self.current_height < self.low_border:
			self.line_state.state = LineState.STATE_LOW
		else:
			self.line_state.state = LineState.STATE_NORMAL
		
		# Add to back
		self.segments.append(self.current_height)
		
		while len(self.segments) > self.length:
			# Remove from front
			self.segments.pop(0)
			
	def draw(self, start_x, start_y):
		x = start_x
		for index in range(len(self.segments)-1, -1, -1):
			pyxel.circ(x, start_y + self.segments[index], self.width, self.color)
			x -= 1
			
			
class LineState():
	STATE_OFF = 0
	STATE_NORMAL = 1
	STATE_HIGH = 2
	STATE_LOW = 3
	
	def __init__(self):
		self.state = LineState.STATE_OFF	