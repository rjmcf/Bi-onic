import pyxel

class Line():
	def __init__(self, length, color, width = 0):
		self.length = length
		self.color = color
		self.width = width
		self.current_height = 0
		self.segments = [self.current_height]
		self.started = False
		
	def toggle_started(self):	
		self.started = not self.started
		
	def update(self, adjustment):
		if not self.started:
			return
			
		self.current_height += adjustment
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
			