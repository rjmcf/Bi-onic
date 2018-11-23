import pyxel
from plugins.window import Window
from plugins.geometry import Point, Proportion2D
from palette_settings import PALETTE
from resource_settings import RESOURCE

# The base for windows used for debugs. Defines a key the user can use to toggle to it
class DebugWindow(Window):
	def __init__(self, title, toggle_key):
		super(DebugWindow, self).__init__(Point(0,0), Proportion2D(1,1))
		self.title = title
		self.toggle_key = toggle_key

# Simply shows the palette currently being used
class PaletteViewer(DebugWindow):
	def __init__(self):
		super(PaletteViewer, self).__init__("Palette Viewer", pyxel.KEY_P)
		
	def draw_palette(self, x, y, col):
		col_val = PALETTE.get_palette()[col]
		hex_col = "#{:06X}".format(col_val)

		pyxel.rect(x, y, x + 8, y + 8, col)
		pyxel.text(x + 16, y + 1, hex_col, 7)
		pyxel.text(x + 3 - (col // 10) * 2, y + 2, "{}".format(col), 7 if col < 6 else 0)
		
	def draw_before_children(self):
		for i in range(16):
			self.draw_palette(self.x + 2 + (i % 4) * 50, self.y + 4 + (i // 4) * 15, i)
	
# The editor can only display the default palette as far as I know. When editing an image,
# you can't actually see how it will look if you use a different palette. This window
# displays an image using the current palette used in game, so you can see how it will
# actually look. You can hot-reload the resource using the Enter key.	
class ImageViewer(DebugWindow):	
	def __init__(self, palette):
		super(ImageViewer,self).__init__("Image Viewer", pyxel.KEY_I)
		self.img_bank = 0
		self.source_top_left_x = 0
		self.source_top_left_y = 0
		self.source_sections_width = 4
		self.source_sections_height = 4
		self.palette = palette
		self.display_top_left_x = 15
		self.display_top_left_y = 20
		
	def update(self):
		super(ImageViewer, self).update()
		if pyxel.btnp(pyxel.KEY_ENTER):
			pyxel.load(RESOURCE)
		
	def draw_before_children(self):
		pyxel.text(self.x,self.y,self.title, 7)
		pyxel.text(self.x,self.y+6, "Showing from (" + str(self.source_top_left_x) + ", " + str(self.source_top_left_y) + ") to (" + str(self.source_top_left_x + self.source_sections_width) + ", " + str(self.source_top_left_y + self.source_sections_height) + ") of image bank " + str(self.img_bank), 7)
		pyxel.text(self.x,self.y+12, "Using palette: {}".format(self.palette.name), 7)
		pyxel.blt(self.x+self.display_top_left_x,self.y+self.display_top_left_y, self.img_bank, self.source_top_left_x * 8, self.source_top_left_y * 8, (self.source_top_left_x + self.source_sections_width) * 8, (self.source_top_left_y + self.source_sections_height)* 8)
		pyxel.rectb(self.x+self.display_top_left_x-1,self.y+self.display_top_left_y-1, self.x+self.display_top_left_x  + self.source_sections_width * 8, self.y+self.display_top_left_y + self.source_sections_height * 8, 7)
		
# Takes an image from the resource and tiles it as wide and tall as you want.
# Can hot-reload the image using the Enter key.	
class Tiler(DebugWindow):
	def __init__(self):
		super(Tiler,self).__init__("Tiler", pyxel.KEY_T) 
		self.img_bank = 0
		self.source_top_left_x = 1*8
		self.source_top_left_y = 6*8
		self.source_width = 5*8 # WHYYY?
		self.source_height = 5*8
		self.repetitions_x = 5
		self.repititions_y = 2
		self.display_top_left_x = 15
		self.display_top_left_y = 20
	
	def update(self):
		super(Tiler,self).update()
		if pyxel.btnp(pyxel.KEY_ENTER):
			pyxel.load(RESOURCE)
			
	def draw_before_children(self):
		for col in range(self.repetitions_x):
			for row in range(self.repititions_y):
				pyxel.blt(self.x + self.display_top_left_x + col * self.source_width,
						  self.y + self.display_top_left_y + row * self.source_height,
						  self.img_bank,
						  self.source_top_left_x,
						  self.source_top_left_y,
						  self.source_top_left_x + self.source_width,
						  self.source_top_left_y + self.source_height)
	
	