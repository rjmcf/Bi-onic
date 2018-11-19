import pyxel

# Represents the line drawn on the graph. 
#TODO Refactor: Should create own LineState?
#TODO Unfinished: Allow changing of speed
#TODO Unfinished: Restrict line to stay within bounds, rendering arrows in the event that 
# 	it doesn't.
#TODO Unfinished: Allow for jumps of more than 1 * width to not break the line.
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
		# Record positions of segments as height above some "middle" value
		self.current_height = 0
		# Record segments to be drawn as the heights they should be drawn at
		self.segments = [self.current_height]
		self.started = False
		
	def reset(self):
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
		
		# Change state depending on current height
		# Remember y increases as you go down the screen
		if self.current_height < -self.high_border:
			self.line_state.state = LineState.STATE_HIGH
		elif self.current_height > -self.low_border:
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
		# Draw backwards from the starting point
		for index in range(len(self.segments)-1, -1, -1):
			pyxel.circ(x, start_y + self.segments[index], self.width, self.color)
			x -= 1
			
# State recording information about the line	
class LineState():
	STATE_OFF = 0
	STATE_NORMAL = 1
	STATE_HIGH = 2
	STATE_LOW = 3
	
	def __init__(self):
		self.state = LineState.STATE_OFF	