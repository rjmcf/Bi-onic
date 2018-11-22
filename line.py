import pyxel

# Represents the line drawn on the graph. 
#TODO Unfinished: Allow changing of speed
#TODO Unfinished: Restrict line to stay within bounds, rendering arrows in the event that 
# 	it doesn't.
#TODO Unfinished: Allow for jumps of more than 1 * width to not break the line.
class Line():
	def __init__(self, game_state):
		self.line_state = LineState()
		self.game_state = game_state
		# Record positions of segments as height above some "middle" value
		self.current_height = 0
		self.velocity = 0
		self.started = False
		
	def set_display(self, line_display):
		self.line_display = line_display
		#TODO Refactor: Maybe not rely on these directly?
		self.low_border = line_display.low_border
		self.low_bound = line_display.low_bound
		self.high_border = line_display.high_border
		
	def reset(self):
		self.current_height = 0
		self.started = False
		self.line_display.reset()
		
	def toggle_started(self):	
		self.started = not self.started
		
	def update(self):
		if pyxel.btnp(pyxel.KEY_SPACE):
			self.toggle_started()
			
		if not self.started:
			self.line_state.state = LineState.STATE_OFF
			return
			
		self.current_height += self.velocity
		self.velocity = 0
		
		# Change state depending on current height
		# Remember y increases as you go down the screen
		if self.current_height < -self.high_border:
			self.line_state.state = LineState.STATE_HIGH
		elif self.current_height > -self.low_bound:
			self.game_state.game_playing = False
		elif self.current_height > -self.low_border:
			self.line_state.state = LineState.STATE_LOW
		else:
			self.line_state.state = LineState.STATE_NORMAL
			
		self.line_display.set_current_height(self.current_height)
		
	# method called to affect the line's velocity, whether by player or environment
	def add_velocity(self, velocity_adjustment):
		self.velocity += velocity_adjustment
		
class LineInterface():
	def __init__(self, line):
		self.line = line
		
	def add_velocity(self, velocity_adjustment):
		self.line.add_velocity(velocity_adjustment)
		
class LineStateInterface():
	def __init__(self, line):
		self.line_state = line.line_state
		
	def get_current_line_state(self):
		return self.line_state.state
			
class LineDisplay():
	def __init__(self, length, low_border, high_border, low_bound, high_bound, color, width = 0):
		self.length = length
		self.low_border = low_border
		self.high_border = high_border
		self.low_bound = low_bound
		self.high_bound = high_bound
		self.color = color
		self.width = width
		# Record segments to be drawn as the heights they should be drawn at
		self.segments = []
		
	def reset(self):
		self.segments = []
		
	def set_current_height(self, current_height):
		# Add to back
		self.segments.append(current_height)
		
		while len(self.segments) > self.length:
			# Remove from front
			self.segments.pop(0)
			
	def draw(self, start_x, start_y):
		x = start_x
		# Draw backwards from the starting point
		for index in range(len(self.segments)-1, -1, -1):
			if self.segments[index] < -self.high_bound:
				if index == len(self.segments)-1:
					pyxel.blt(x,start_y - self.high_bound, 0, 32,0, 7,8, 0)
			else:
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