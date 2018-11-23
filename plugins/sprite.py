import pyxel

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