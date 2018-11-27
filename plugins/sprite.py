import pyxel
from plugins.geometry import Vector

class Sprite():
	def __init__(self, source_point, source_size, img_bank, transpar_col = None):
		self.source_point = source_point
		self.source_size = source_size
		self.img_bank = img_bank
		self.transpar_col = transpar_col
		
	def draw(self, at, centered_x = False, centered_y = False):
		if centered_x:
			at.x -= self.source_size.x * 0.5
		if centered_y:
			at.y -= self.source_size.y * 0.5
		pyxel.blt(*at, self.img_bank, *self.source_point, *self.source_size, self.transpar_col)
		
class TextSprite():
	def __init__(self, text, col):
		self.text = text
		self.col = col
		self.char_width = 4
		self.char_height = 5
		self.pixel_width = len(text) * self.char_width
		self.pixel_height = self.char_height
		
	def draw(self, at, centered_x = False, centered_y = False, colour = None):
		if centered_x:
			at = at.translate(Vector(-self.pixel_width/2,0))
		if centered_y:
			at = at.translate(Vector(0, -self.pixel_height/2))
		pyxel.text(*at, self.text, colour if colour else self.col)