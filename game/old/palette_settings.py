import pyxel

# Represents a colour palette in code
# wraps a list of 16 colour codes and a name
class Palette():
	def __init__(self, name : str) -> None:
		self.name = name

		self.internal_palette : list[int] = [0 for i in range(16)]#pyxel.DEFAULT_PALETTE

	# Let's you overwrite a colour in the palette
	def __setitem__(self, index : int, item : int) -> None:
		if isinstance(index, tuple):
			raise TypeError("only one index expected")

		self.internal_palette[index] = item

	# Used when we want to actually use the palette to render something
	def get_palette(self):
		return self.internal_palette

# The standard palette to be used while playing the game
game_palette = Palette("game")
game_palette[1] = 0x7e2553
game_palette[2] = 0x8b4226
game_palette[10] = 0x000000 # Animated colour
game_palette[11] = 0xdd9060
game_palette[14] = 0xffec27

# The palette used to render characters for close up images on social media
character_palette = Palette("character")
character_palette[2] = 0x8b4226
character_palette[10] = 0xaa004d
character_palette[11] = 0xdd9060

# Spare palette used for testing stuff.
test_palette = Palette("test")
test_palette[13] = 0x8759ad

# The actual palette being used currently
# This is set when we initialise the game, so will need to quit and restart to have effect.
PALETTE = game_palette
