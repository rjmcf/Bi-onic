import pyxel
from plugins.window import Window
from plugins.geometry import Point, Size, Vector, Proportion2D
from plugins.sprite import Sprite, TextSprite
from palette_settings import PALETTE
from resource_settings import RESOURCE

# The base for windows used for debugs. Defines a key the user can use to toggle to it,
# which defines the equality relation
class DebugWindow(Window):
	def __init__(self, title, toggle_key):
		super(DebugWindow, self).__init__(Point(0,0), Proportion2D(1,1))
		self.title = title
		self.toggle_key = toggle_key
		
	def __eq__(self, other):
		# We only want to compare ourselves by key with other Debug windows
		if isinstance(other, DebugWindow):
			return self.toggle_key == other.toggle_key
		else:
			return super(DebugWindow, self).__eq__(other)
		
	def __hash__(self):
		return self.toggle_key
		
# Allows for debugging of TextSprites
class TextImager(DebugWindow):
	def __init__(self):
		super(TextImager, self).__init__("Text Imager", pyxel.KEY_S)
		self.text_sprite = TextSprite("Sample Text", 8)
		
	def draw_before_children(self):	
		pyxel.line(*self.size.scale2D(Size(0.5,0)), *self.size.scale2D(Size(0.5,1)), 7)
		pyxel.line(*self.size.scale2D(Size(0,0.5)), *self.size.scale2D(Size(1,0.5)), 7)
		self.text_sprite.draw(self.corner.br_of(self.size.scale2D(Size(0.5,0.5))), True, True)
		
		
# Shows a representation of an affector, input (0,1), output (0,1)
class GraphImager(DebugWindow):
	def __init__(self):
		super(GraphImager, self).__init__("Graph Imager", pyxel.KEY_G)
		self.graph_tl = Point(10,10)
		self.graph_size = Size(100, 70)
		self.cutoff = 0.9
		
	def f(self, x):
		if x < self.cutoff:
			return self.up_curve(x / self.cutoff)
		return -self.up_curve((x-self.cutoff) / (1-self.cutoff))
			
	def up_curve(self, t):
		return t*(1-t)
		
	def g(self, x):
		return x * (1-x)
		
	def h(self, x):
		return -self.g(x)
		
	def draw_before_children(self):
		pyxel.rectb(*self.graph_tl, *self.graph_tl.br_of(self.graph_size), 7)
		pyxel.rectb(*self.graph_tl.br_of(Point(0, self.graph_size.y)), *self.graph_tl.br_of(self.graph_size.scale2D(Size(1,2))), 7)
		self.draw_func_with_col(self.f, 8)
		self.draw_func_with_col(self.g, 9)
		self.draw_func_with_col(self.h, 10)
		
			
	def draw_func_with_col(self, func, col):
		for x in range(self.graph_size.x):
			current_y = self.graph_size.y * func(x / self.graph_size.x)
			current_y = self.graph_tl.y + self.graph_size.y - current_y
			current_x = self.graph_tl.x + x
			if x == 0:
				previous_y = current_y
				previous_x = current_x
			pyxel.line(previous_x, previous_y, current_x, current_y, col)
			previous_x = current_x
			previous_y = current_y
		

# Simply shows the palette currently being used
class PaletteViewer(DebugWindow):
	def __init__(self):
		super(PaletteViewer, self).__init__("Palette Viewer", pyxel.KEY_O)
		
	def draw_palette(self, x, y, col):
		col_val = PALETTE.get_palette()[col]
		hex_col = "#{:06X}".format(col_val)

		pyxel.rect(x, y, x + 8, y + 8, col)
		pyxel.text(x + 16, y + 1, hex_col, 7)
		pyxel.text(x + 3 - (col // 10) * 2, y + 2, "{}".format(col), 7 if col < 6 else 0)
		
	def draw_before_children(self):
		for i in range(16):
			self.draw_palette(self.corner.x + 2 + (i % 4) * 50, self.corner.y + 4 + (i // 4) * 15, i)
	
# The editor can only display the default palette as far as I know. When editing an image,
# you can't actually see how it will look if you use a different palette. This window
# displays an image using the current palette used in game, so you can see how it will
# actually look. You can hot-reload the resource using the Enter key.	
class ImageViewer(DebugWindow):	
	def __init__(self, palette):
		super(ImageViewer,self).__init__("Image Viewer", pyxel.KEY_I)
		self.img_bank = 0
		self.source_top_left = Vector(0, 12)
		self.source_sections = Size(4,8)
		self.palette = palette
		self.display_top_left = Vector(15,20)
		
	def update(self):
		super(ImageViewer, self).update()
		if pyxel.btnp(pyxel.KEY_ENTER):
			pyxel.load(RESOURCE)
		
	def draw_before_children(self):
		pyxel.text(*self.corner,self.title, 7)
		pyxel.text(*self.corner.br_of(Size(0,6)), "Showing from (" + str(self.source_top_left.x) + ", " + str(self.source_top_left.y) + ") to (" + str(self.source_top_left.x + self.source_sections.x) + ", " + str(self.source_top_left.y + self.source_sections.y) + ") of image bank " + str(self.img_bank), 7)
		pyxel.text(*self.corner.br_of(Size(0,12)), "Using palette: {}".format(self.palette.name), 7)
		pyxel.blt(*self.corner.translate(self.display_top_left), self.img_bank, *self.source_top_left.scale(8), *self.source_top_left.add(self.source_sections).scale(8))
		pyxel.rectb(*self.corner.translate(self.display_top_left.add(Vector(-1,-1))), *self.corner.translate(self.display_top_left).br_of(self.source_sections.scale(8)), 7)
		
# Takes an image from the resource and tiles it as wide and tall as you want.
# Can hot-reload the image using the Enter key.	
class Tiler(DebugWindow):
	def __init__(self):
		super(Tiler,self).__init__("Tiler", pyxel.KEY_T) 
		self.sprite = Sprite(Point(1*8,6*8), Size(5*8,5*8), 0)
		self.source_size = self.sprite.source_size
		self.repetitions_x = 3
		self.repetitions_y = 3
		self.display_top_left = Vector(20,20)
	
	def update(self):
		super(Tiler,self).update()
		if pyxel.btnp(pyxel.KEY_ENTER):
			pyxel.load(RESOURCE)
			
	def draw_before_children(self):
		for col in range(self.repetitions_x):
			for row in range(self.repetitions_y):
				self.sprite.draw(self.corner.br_of(self.source_size.scale2D(Vector(col,row))).translate(self.display_top_left))