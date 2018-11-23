from plugins.geometry import Point

class TopLevelWindow():
	def __init__(self, size):
		self.size = size
		self.windows = []
		
	def update(self):
		for window in self.windows:
			window.update()
	
	def draw(self):
		for window in self.windows:
			window.draw(Point(0,0), self.size)

# Represents a game-window in code.
# Defines itself in terms of proportions of its parent that it takes up,
# i.e. how far in x and y the top left corner is, and how much width and height is used.
# Windows are hierarchical, and so have a list of child_windows that they manage.
#TODO Investigate: Validate on whether stuff is outside the parent?
class Window():
	def __init__(self, corner_prop, size_prop, parent_corner = None, parent_size = None):
		self.corner_prop = corner_prop
		self.size_prop = size_prop
		
		if None not in [parent_corner, parent_size]:
			self.calculate_dimensions(parent_corner, parent_size)
		
		self.child_windows = []
		
	def calculate_dimensions(self, parent_corner, parent_size):
		self.corner = parent_corner.br_of(parent_size.scale2D(self.corner_prop))
		self.size = parent_size.scale2D(self.size_prop)
		
	# Called every frame to update the contents	
	def update(self):
		for window in self.child_windows:
			window.update()
		
	def draw(self, parent_corner, parent_size):
		self.calculate_dimensions(parent_corner, parent_size)
		self.draw_before_children()
		for child in self.child_windows:
			child.draw(self.corner, self.size)
		self.draw_after_children()
		
	# Overriden to draw things for this specific child before further children
	def draw_before_children(self):
		pass
		
	# Overriden to draw things for this specific child after further children
	def draw_after_children(self):
		pass