class Window():
	def __init__(self, x = 0,y = 0, width = 0,height = 0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
		# instances of ChildWindow
		self.child_windows = []
			
	def update(self):
		for window in self.child_windows:
			window.update()
			
	def draw(self):
		for child in self.child_windows:
			child.draw(self.x, self.y, self.width, self.height)
			
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
		
		
class DebugWindow(ChildWindow):
	def __init__(self, title, toggle_key):
		super(DebugWindow, self).__init__(0,0, 1,1)
		self.title = title
		self.toggle_key = toggle_key