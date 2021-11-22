import pyxel
from plugins.geometry import Proportion2D
from plugins.window import Window
from typing import Optional

# Represents a bar that can be filled. Bars can be horizontal or vertical, and fill in
# either direction. Stores how much it's filled as a percentage.
class FillableBar(Window):
	def __init__(self, corner_prop : Proportion2D, size_prop : Proportion2D, is_vertical : bool, fill_positive : bool, back_colour : int, fill_colour : int, border_colour : Optional[int] = None) -> None:
		super(FillableBar, self).__init__(corner_prop, size_prop)
		self.percent_full : float = 0
		self.is_vertical = is_vertical
		self.fill_positive = fill_positive
		self.back_colour = back_colour
		self.fill_colour = fill_colour
		self.border_colour = border_colour

	# Method used to add an amount to the bar.
	def adjust_bar(self, percent_difference : float) -> None:
		self.set_bar(self.percent_full + percent_difference)

	# Method used to set amount for bar
	def set_bar(self, percent_full : float) -> None:
		self.percent_full = percent_full
		self.percent_full = min(self.percent_full, 1)
		self.percent_full = max(0, self.percent_full)

	def is_empty(self) -> bool:
		return self.percent_full <= 0

	def is_full(self) -> bool:
		return self.percent_full >= 1

	def draw_before_children(self) -> None:
		pyxel.rect(*self.corner, *self.size, self.back_colour)
		if self.is_vertical:
			top_left_x = self.corner.x
			top_left_y = self.corner.y if self.fill_positive else int(self.corner.y + (1-self.percent_full) * self.size.y)
			width = self.size.x
			height = self.percent_full * self.size.y
		else:
			top_left_x = self.corner.x if self.fill_positive else int(self.corner.x + (1-self.percent_full) * self.size.x)
			top_left_y = self.corner.y
			width = self.percent_full * self.size.x
			height = self.size.y
		pyxel.rect(top_left_x, top_left_y, width, height, self.fill_colour)

		if self.border_colour != None:
			pyxel.rectb(*self.corner, *self.size, self.border_colour)
