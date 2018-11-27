import pyxel

# Represents a colour palette in code
# wraps a list of 16 colour codes and a name
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
	
	# Used when we want to actually use the palette to render something
	def get_palette(self):
		return [self.c0,  self.c1,  self.c2,  self.c3,
				self.c4,  self.c5,  self.c6,  self.c7,
				self.c8,  self.c9,  self.c10, self.c11,
				self.c12, self.c13, self.c14, self.c15]

# The standard palette to be used while playing the game
game_palette = Palette("game")
game_palette.c1 = 0x7e2553
game_palette.c2 = 0x8b4226
game_palette.c10 = 0xaa004d
game_palette.c11 = 0xdd9060
game_palette.c14 = 0xffec27

# The palette used to render characters for close up images on social media
character_palette = Palette("character")
character_palette.c2 = 0x8b4226
character_palette.c10 = 0xaa004d
character_palette.c11 = 0xdd9060

# Spare palette used for testing stuff.
test_palette = Palette("test")
test_palette.c13 = 0x8759ad 

# The actual palette being used currently
# This is set when we initialise the game, so will need to quit and restart to have effect.
PALETTE = game_palette