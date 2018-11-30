import pyxel
from plugins.geometry import Vector, Size

# Determines the relation of the origin to the sprite.
# e.g. x = LEFT, y = TOP means that the origin is in the top left of the image
#TODO Refactor: Should we store state actually? Gives us type checking...
class Anchor:
	TOP = 0
	MIDDLE = 1
	BOTTOM = 2
	LEFT = 3
	RIGHT = 4
	
def justify(at, size, anchor_x, anchor_y):
	if isinstance(anchor_x, bool) or isinstance(anchor_y, bool):
		print("anchor values must be from Anchor")
		pyxel.quit()
		
	if anchor_x == Anchor.LEFT:
		x_adjust = 0
	elif anchor_x == Anchor.MIDDLE:
		x_adjust = -size.x * 0.5
	elif anchor_x == Anchor.RIGHT:
		x_adjust = -size.x
	else:
		print("Invalid anchor_x value:", anchor_x)
		pyxel.quit()
			
	if anchor_y == Anchor.TOP:
		y_adjust = 0
	elif anchor_y == Anchor.MIDDLE:
		y_adjust = -size.y * 0.5
	elif anchor_y == Anchor.BOTTOM:
		y_adjust = -size.y
	else:
		print("Invalid anchor_y value:", anchor_y)
		pyxel.quit()
		
	return at.translate(Vector(x_adjust, y_adjust))

# Represents an image that can be drawn
class Sprite():
	def __init__(self, source_point, source_size, img_bank, transpar_col = None):
		self.source_point = source_point
		self.source_size = source_size
		self.img_bank = img_bank
		self.transpar_col = transpar_col
		
	def draw(self, at, anchor_x = Anchor.LEFT, anchor_y = Anchor.TOP):
		at = justify(at, self.source_size, anchor_x, anchor_y)
			
		pyxel.blt(*at, self.img_bank, *self.source_point, *self.source_size, self.transpar_col)
		
# Represents a bit of text that can be drawn
# Currently only supports a single line
class TextSprite():
	def __init__(self, text, col):
		self.text = text
		self.col = col
		self.char_width = 4
		self.char_height = 6
		self.calculate_sizes()
		
	def calculate_sizes(self):
		self.size = Size(len(self.text) * self.char_width, self.char_height)
		
	def draw(self, at, anchor_x = Anchor.LEFT, anchor_y = Anchor.TOP, colour = None):
		at = justify(at, self.size, anchor_x, anchor_y)
		pyxel.text(*at, self.text, colour if colour else self.col)