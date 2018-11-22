class TopLevelWindow():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.windows = []
		
	def update(self):
		for window in self.windows:
			window.update()
	
	def draw(self):
		for window in self.windows:
			window.draw(0,0, self.width, self.height)

# Represents a game-window in code.
# Defines itself in terms of proportions of its parent that it takes up,
# i.e. how far in x and y the top left corner is, and how much width and height is used.
# Windows are hierarchical, and so have a list of child_windows that they manage.
#TODO Investigate: Validate on whether stuff is outside the parent?
class Window():
	def __init__(self, x_prop, y_prop, width_prop, height_prop, parent_x = None, parent_y = None, parent_width = None, parent_height = None):
		self.x_prop = x_prop
		self.y_prop = y_prop
		self.width_prop = width_prop
		self.height_prop = height_prop
		
		if None not in [parent_x, parent_y, parent_width, parent_height]:
			self.calculate_dimensions(parent_x, parent_y, parent_width, parent_height)
		
		self.child_windows = []
		
	def calculate_dimensions(self, parent_x, parent_y, parent_width, parent_height):
		self.x = parent_x + parent_width * self.x_prop
		self.y = parent_y + parent_height * self.y_prop
		self.width = parent_width * self.width_prop
		self.height = parent_height * self.height_prop
		
	# Called every frame to update the contents	
	def update(self):
		for window in self.child_windows:
			window.update()
		
	def draw(self, parent_x, parent_y, parent_width, parent_height):
		self.calculate_dimensions(parent_x, parent_y, parent_width, parent_height)
		self.draw_before_children()
		for child in self.child_windows:
			child.draw(self.x, self.y, self.width, self.height)
		self.draw_after_children()
		
	# Overriden to draw things for this specific child before further children
	def draw_before_children(self):
		pass
		
	# Overriden to draw things for this specific child after further children
	def draw_after_children(self):
		pass