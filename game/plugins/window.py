from plugins.geometry import Point, Proportion2D, Size
from typing import Optional

# Represents a game-window in code.
# Defines itself in terms of proportions of its parent that it takes up,
# i.e. how far in x and y the top left corner is, and how much width and height is used.
# Windows are hierarchical, and so have a list of child_windows that they manage.
#TODO Investigate: Validate on whether stuff is outside the parent?
class Window():
	def __init__(self, corner_prop : Proportion2D, size_prop : Proportion2D, parent_corner : Optional[Point] = None, parent_size : Optional[Size] = None) -> None:
		self.corner_prop = corner_prop
		self.size_prop = size_prop

		if parent_corner is not None and parent_size is not None:
			self.calculate_dimensions(parent_corner, parent_size)

		self.child_windows : list[Window] = []

	def calculate_dimensions(self, parent_corner : Point, parent_size : Size) -> None:
		self.corner = parent_corner.br_of(parent_size.scale2D(self.corner_prop))
		self.size = parent_size.scale2D(self.size_prop)

	def update(self) -> None:
		for window in self.child_windows:
			window.update()

	def draw(self, parent_corner : Point, parent_size : Size) -> None:
		self.calculate_dimensions(parent_corner, parent_size)
		self.draw_before_children()
		for child in self.child_windows:
			child.draw(self.corner, self.size)
		self.draw_after_children()

	# Overriden to draw things for this specific child before further children
	def draw_before_children(self) -> None:
		pass

	# Overriden to draw things for this specific child after further children
	def draw_after_children(self) -> None:
		pass

# Represents the TopLevelWindow, ie, the parent of all other windows
class TopLevelWindow():
	def __init__(self, size : Size) -> None:
		self.size = size
		self.windows : list[Window] = []

	def update(self) -> None:
		for window in self.windows:
			window.update()

	def draw(self) -> None:
		for window in self.windows:
			window.draw(Point(0,0), self.size)
