import pyxel
from plugins.window import ChildWindow

class FillableBar(ChildWindow):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, is_vertical, fill_positive, back_colour, fill_colour, border_colour = None):
		super(FillableBar, self).__init__(x_prop, y_prop, width_prop, height_prop)
		self.percent_full = 0
		self.is_vertical = is_vertical
		self.fill_positive = fill_positive
		self.back_colour = back_colour
		self.fill_colour = fill_colour
		self.border_colour = border_colour
		
	def adjust_bar(self, percent_difference):
		self.percent_full += percent_difference
		self.percent_full = min(self.percent_full, 1)
		self.percent_full = max(0, self.percent_full)
		
	def is_empty(self):
		return self.percent_full == 0
		
	def draw_before_children(self):
		pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.back_colour)
		if self.is_vertical:
			top_left_x = self.x
			top_left_y = self.y if self.fill_positive else self.y + (1-self.percent_full) * self.height
			bottom_right_x = self.x + self.width
			bottom_right_y = self.y + self.percent_full * self.height if self.fill_positive else self.y + self.height
		else:
			top_left_x = self.x if self.fill_positive else self.x + (1-self.percent_full) * self.width
			top_left_y = self.y 
			bottom_right_x = self.x + self.percent_full * self.width if self.fill_positive else self.x + self.width
			bottom_right_y = self.y + self.height
		pyxel.rect(top_left_x, top_left_y, bottom_right_x, bottom_right_y, self.fill_colour)
		
		if self.border_colour != None:
			pyxel.rectb(self.x, self.y, self.x + self.width, self.y + self.height, self.border_colour)