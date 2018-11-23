import pyxel
from plugins.window import Window

# Represents a bar that can be filled. Bars can be horizontal or vertical, and fill in 
# either direction. Stores how much it's filled as a percentage.
class FillableBar(Window):
	def __init__(self, corner_prop, size_prop, is_vertical, fill_positive, back_colour, fill_colour, border_colour = None):
		super(FillableBar, self).__init__(corner_prop, size_prop)
		self.percent_full = 0
		self.is_vertical = is_vertical
		self.fill_positive = fill_positive
		self.back_colour = back_colour
		self.fill_colour = fill_colour
		self.border_colour = border_colour
		
	# Method used to add an amount to the bar.
	def adjust_bar(self, percent_difference):
		self.set_bar(self.percent_full + percent_difference)
		
	# Method used to set amount for bar
	def set_bar(self, percent_full):
		self.percent_full = percent_full
		self.percent_full = min(self.percent_full, 1)
		self.percent_full = max(0, self.percent_full)
		
	def is_empty(self):
		return self.percent_full <= 0
		
	def is_full(self):
		return self.percent_full >= 1
		
	def draw_before_children(self):
		pyxel.rect(*self.corner, *self.corner.br_of(self.size), self.back_colour)
		if self.is_vertical:
			top_left_x = self.corner.x
			top_left_y = self.corner.y if self.fill_positive else self.corner.y + (1-self.percent_full) * self.size.y
			bottom_right_x = self.corner.x + self.size.x
			bottom_right_y = self.corner.y + self.percent_full * self.size.y if self.fill_positive else self.corner.y + self.size.y
		else:
			top_left_x = self.corner.x if self.fill_positive else self.corner.x + (1-self.percent_full) * self.width
			top_left_y = self.corner.y 
			bottom_right_x = self.corner.x + self.percent_full * self.width if self.fill_positive else self.corner.x + self.width
			bottom_right_y = self.corner.y + self.size.y
		pyxel.rect(top_left_x, top_left_y, bottom_right_x, bottom_right_y, self.fill_colour)
		
		if self.border_colour != None:
			pyxel.rectb(*self.corner, *self.corner.br_of(self.size), self.border_colour)