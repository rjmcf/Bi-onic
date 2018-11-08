import pyxel

class Palette():
	def __init__(self, name):
		self.name = name
		
		self.c0  = pyxel.DEFAULT_PALETTE[0]
		self.c1  = pyxel.DEFAULT_PALETTE[1]
		self.c2  = pyxel.DEFAULT_PALETTE[2]
		self.c3  = pyxel.DEFAULT_PALETTE[3]
	
		self.c4  = pyxel.DEFAULT_PALETTE[4]
		self.c5  = pyxel.DEFAULT_PALETTE[5]
		self.c6  = pyxel.DEFAULT_PALETTE[6]
		self.c7  = pyxel.DEFAULT_PALETTE[7]
	
		self.c8  = pyxel.DEFAULT_PALETTE[8]
		self.c9  = pyxel.DEFAULT_PALETTE[9]
		self.c10 = pyxel.DEFAULT_PALETTE[10]
		self.c11 = pyxel.DEFAULT_PALETTE[11]
		
		self.c12 = pyxel.DEFAULT_PALETTE[12]
		self.c13 = pyxel.DEFAULT_PALETTE[13]
		self.c14 = pyxel.DEFAULT_PALETTE[14]
		self.c15 = pyxel.DEFAULT_PALETTE[15]
	
	def get_palette(self):
		return [self.c0,  self.c1,  self.c2,  self.c3,
				self.c4,  self.c5,  self.c6,  self.c7,
				self.c8,  self.c9,  self.c10, self.c11,
				self.c12, self.c13, self.c14, self.c15]

game_palette = Palette("game")

character_palette = Palette("character")
character_palette.c2 = 0x8b4226
character_palette.c10 = 0xaa004d
character_palette.c11 = 0xdd9060
# CloudCall 8759ad

PALETTE = game_palette