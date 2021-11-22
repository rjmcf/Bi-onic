import pyxel
from plugins.window import Window
from plugins.geometry import Point, Proportion2D, Size
from line import Line, LineDisplay

# Just fills itself with a given colour
class DangerRegion(Window):
	def __init__(self, x_prop : float, y_prop : float, width_prop : float, height_prop : float, colour : int) -> None:
		super(DangerRegion, self).__init__(Proportion2D(x_prop, y_prop), Proportion2D(width_prop, height_prop))
		self.colour = colour

	def draw_before_children(self) -> None:
		pyxel.rect(*self.corner, *self.size, self.colour)

# The window within which the graph is drawn.
class GraphWindow(Window):
	def __init__(self, parent_corner : Point, parent_size : Size) -> None:
		super(GraphWindow, self).__init__(Proportion2D(0,0.4), Proportion2D(1,0.6), parent_corner, parent_size)
		self.colour = 6
		self.start_prop = Proportion2D(1/2, 1/2)
		self.high_region_prop = 2/5
		self.low_region_prop = 1/5
		self.line_display = LineDisplay(150,
										-(1-self.start_prop.y-self.low_region_prop)*self.size.y,
										(self.start_prop.y-self.high_region_prop)*self.size.y,
										(self.start_prop.y-1)*self.size.y,
										self.start_prop.y*self.size.y,
										12, 2)
		self.danger_high = DangerRegion(0,0, 1,self.high_region_prop, 9)
		self.danger_low = DangerRegion(0,1-self.low_region_prop, 1,self.low_region_prop, 8)
		self.child_windows = [self.danger_high, self.danger_low]

	def set_line_display(self, line : Line) -> None:
		line.set_display(self.line_display)

	def update(self) -> None:
		super(GraphWindow, self).update()

	def draw_before_children(self) -> None:
		pyxel.rect(*self.corner, *self.size, self.colour)

	def draw_after_children(self) -> None:
		self.line_display.draw(self.corner.br_of(self.size.scale2D(self.start_prop)))
