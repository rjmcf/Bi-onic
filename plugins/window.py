# Represents a game-window in code. Defined by the screen-position of the top-left corner,
# a width, and a height. 
# Windows are hierarchical, and so have a list of child_windows that it manages.
class Window():
	def __init__(self, x = 0,y = 0, width = 0,height = 0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
		# instances of ChildWindow
		self.child_windows = []
		
	# Called every frame to update the contents	
	def update(self):
		for window in self.child_windows:
			window.update()
			
	# Called every frame to draw the contents.
	def draw(self):
		for child in self.child_windows:
			child.draw(self.x, self.y, self.width, self.height)
	
# Defines itself in terms of proportions of parents that it takes up,
# i.e. how far in x and y the top left corner is, and how much width and height is used.
#TODO Refactor: Merge into Window class?
#TODO Investigate: Validate on whether stuff is outside the parent?
class ChildWindow(Window):
	def __init__(self, x_prop, y_prop, width_prop, height_prop):
		super(ChildWindow, self).__init__()
		self.x_prop = x_prop
		self.y_prop = y_prop
		self.width_prop = width_prop
		self.height_prop = height_prop
		
	def draw(self, parent_x, parent_y, parent_width, parent_height):
		self.x = parent_x + parent_width * self.x_prop
		self.y = parent_y + parent_height * self.y_prop
		self.width = parent_width * self.width_prop
		self.height = parent_height * self.height_prop
		self.draw_before_children()
		super(ChildWindow, self).draw()
		self.draw_after_children()
		
	# Overriden to draw things for this specific child before further children
	def draw_before_children(self):
		pass
		
	# Overriden to draw things for this specific child after further children
	def draw_after_children(self):
		pass