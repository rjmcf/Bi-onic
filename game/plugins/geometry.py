# Represents something that has an x and a y component, which can be unpacked using *
# to get (x,y)
class Unpackable2D():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	# Enables us to use *
	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError() 
	
# Represents a Point in 2D space
class Point(Unpackable2D):
	def __init__(self, x, y):
		super(Point, self).__init__(x,y)
		
	# Get the bottom-right corner of the box defined with this point as the top-left,
	# and the dimensions determined by size.
	def br_of(self, size):
		return Point(self.x + size.x, self.y + size.y)
		
	# Get the top-left corner of the box defined with this point as the bottom-right,
	# and the dimensions determined by size.
	def tl_of(self, size):
		return Point(self.x - size.x, self.y - size.y)
		
	# Return the Point you get when you translate this point by the given Vector
	def translate(self, vector):
		return Point(self.x + vector.x, self.y + vector.y)
		
# Represents a displacement in 2D space.
class Vector(Unpackable2D):
	def __init__(self, x, y):
		super(Vector, self).__init__(x,y)
		
	# Get this vector, scaled by the given float
	def scale(self, scale):
		return Vector(self.x * scale, self.y * scale)
		
	# Get the sum of this vector and the other vector
	def add(self, vector):
		return Vector(self.x + vector.x, self.y + vector.y)
	
# Represents the dimensions of a rectangle
class Size(Unpackable2D):
	def __init__(self, x, y):
		super(Size, self).__init__(x,y)
		
	# Return the rectangle you get when you apply the supplied 2D scale to this rectangle
	def scale2D(self, scale):
		return Size(self.x * scale.x, self.y * scale.y)
		
	# Return the rectangle you get when you scale this one by the supplied float.
	def scale(self, scale):
		return Size(self.x * scale, self.y * scale)
	
# Represents a scale factor in 2D, with components clamped between 0 and 1	
class Proportion2D(Unpackable2D):
	def __init__(self, x, y):
		super(Proportion2D, self).__init__(max(0, min(1, x)), max(0, min(1, y)))