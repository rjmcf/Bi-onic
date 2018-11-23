class Unpackable2D():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError() 
	

class Point(Unpackable2D):
	def __init__(self, x, y):
		super(Point, self).__init__(x,y)
		
	# Get the bottom right corner of the box defined with this point as the top-left,
	# and the dimensions determined by size.
	def br_of(self, size):
		return Point(self.x + size.x, self.y + size.y)
		
	def tl_of(self, size):
		return Point(self.x - size.x, self.y - size.y)
		
	def translate(self, vector):
		return Point(self.x + vector.x, self.y + vector.y)
		
class Vector(Unpackable2D):
	def __init__(self, x, y):
		super(Vector, self).__init__(x,y)
		
	def scale(self, scale):
		return Vector(self.x * scale, self.y * scale)
		
	def add(self, vector):
		return Vector(self.x + vector.x, self.y + vector.y)
	
class Size(Unpackable2D):
	def __init__(self, x, y):
		super(Size, self).__init__(x,y)
		
	def scale2D(self, proportion2D):
		return Size(self.x * proportion2D.x, self.y * proportion2D.y)
		
	def scale(self, scale):
		return Size(self.x * scale, self.y * scale)
		
class Proportion2D(Unpackable2D):
	def __init__(self, x, y):
		super(Proportion2D, self).__init__(max(0, min(1, x)), max(0, min(1, y)))