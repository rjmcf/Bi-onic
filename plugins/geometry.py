class TwoDUnpackable():
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
	

class Point(TwoDUnpackable):
	def __init__(self, x, y):
		super(Point, self).__init__(x,y)
	
class Size(TwoDUnpackable):
	def __init__(self, x, y):
		super(Size, self).__init__(x,y)
		
class Scale(TwoDUnpackable):
	def __init__(self, x, y):
		super(Scale, self).__init__(max(0, min(1, x)), max(0, min(1, y)))