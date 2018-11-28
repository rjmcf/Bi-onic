import pyxel
from plugins.geometry import Point, Size
from plugins.sprite import Sprite, Anchor

# Possible states for the line	
class LineState():
	STATE_NORMAL = 0
	STATE_HIGH = 1
	STATE_LOW = 2

# Represents the line drawn on the graph. 
#TODO Unfinished: Allow changing of speed
#TODO Unfinished: Allow for jumps of more than 1 * width to not break the line.
class Line():
	def __init__(self, game_state):
		self.line_state = LineState.STATE_NORMAL
		self.game_state = game_state
		# Record positions of segments as height above some "middle" value
		self.current_height = 0
		self.velocity = 0
		
	def set_display(self, line_display):
		self.line_display = line_display
		self.low_border = line_display.low_border
		self.low_bound = line_display.low_bound
		self.high_border = line_display.high_border
		
	def reset(self):
		self.current_height = 0
		self.line_display.reset()
		
	def update(self):
		self.current_height += self.velocity
		self.velocity = 0
		
		# Change state depending on current height
		# Remember y increases as you go down the screen
		if self.current_height < -self.high_border:
			self.line_state = LineState.STATE_HIGH
		elif self.current_height > -self.low_bound:
			self.game_state.game_playing = False
		elif self.current_height > -self.low_border:
			self.line_state = LineState.STATE_LOW
		else:
			self.line_state = LineState.STATE_NORMAL
			
		self.line_display.set_current_height(self.current_height)
		
	# method called to affect the line's velocity, whether by player or environment
	def add_velocity(self, velocity_adjustment):
		self.velocity += velocity_adjustment
		
# Interface used by the controller to add velocity to the line
class LineInterface():
	def __init__(self, line):
		self.line = line
		
	def add_velocity(self, velocity_adjustment):
		self.line.add_velocity(velocity_adjustment)
		
# Interface used to get the current state of the line
class LineStateInterface():
	def __init__(self, line):
		self.line = line
		
	def get_current_line_state(self):
		return self.line.line_state
		
# The visual representation of the Line	
class LineDisplay():
	def __init__(self, length, low_border, high_border, low_bound, high_bound, color, width = 0):
		self.length = length
		self.low_border = low_border
		self.high_border = high_border
		self.low_bound = low_bound
		self.high_bound = high_bound
		self.color = color
		self.width = width
		self.arrow_sprite = Sprite(Point(32,0), Size(7,8), 0, 0)
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
			
	def draw(self, start):
		x = start.x
		# Draw backwards from the starting point
		for index in range(len(self.segments)-1, -1, -1):
			if self.segments[index] < -self.high_bound:
				if index == len(self.segments)-1:
					self.arrow_sprite.draw(Point(x,start.y - self.high_bound), Anchor.MIDDLE)
			else:
				pyxel.circ(x, start.y + self.segments[index], self.width, self.color)
			x -= 1