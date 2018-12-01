import pyxel
from plugins.geometry import Point, Proportion2D, Size
from plugins.window import Window
from plugins.sprite import Sprite, TextSprite, Anchor

class MainMenuOption(TextSprite):
	def __init__(self, text, col, func):
		super(MainMenuOption, self).__init__(text, col)
		self.func = func
		
class StatefulMainMenuOption(MainMenuOption):
	def __init__(self, text, format, col, func):
		super(StatefulMainMenuOption, self).__init__(text.format(format), col, func)
		self.unformatted_text = text
		self.format = format
		
	def update_format(self, format):
		self.format = format
	
	def draw(self, at, anchor_x = Anchor.LEFT, anchor_y = Anchor.TOP, colour = None):
		self.text = self.unformatted_text.format(self.format)
		self.calculate_sizes()
		super(StatefulMainMenuOption, self).draw(at, anchor_x, anchor_y, colour)
		
		
# Represents both the logic and the display of the Main Menu.
# Although not separating them is a break from my convention, the resulting code is much
# neater in this case, and there's no need for syncing up what the various menu options 
# can be across two different classes.
class MainMenu(Window):
	def __init__(self, start_game_interface):
		super(MainMenu, self).__init__(Point(0,0), Proportion2D(1,1))	
		self.start_game_interface = start_game_interface
		self.bg_col = 0
		self.text_col = 7
		self.selected_col = 14
		self.character_sprite = Sprite(Point(0,0), Size(32,40), 0, 0)
		self.tutorial_menu_option = StatefulMainMenuOption("Tutorial: {}", "Yes", self.text_col, lambda main_menu: main_menu.update_tutorial_state())
		self.options = [
			MainMenuOption("Start Game", self.text_col, lambda main_menu: main_menu.start_game_interface.start_game()),
			self.tutorial_menu_option,
			MainMenuOption("Quit", self.text_col, lambda main_menu: pyxel.quit())
		]	
		self.num_options = len(self.options)
		self.current_option = 0
		self.tutorial_active = True
		self.credit_text = TextSprite("By Robin McFarland: @RjmcfDev", 7)
		self.title = Sprite(Point(0,91), Size(67,23), 0, 0)
		self.animated_col = 10
		self.animated_col_list = [11,9,8,8,9]
		self.current_animated_col_index = 0
		self.frame_gap = 5
		
	def update_tutorial_state(self):
		self.tutorial_active = not self.tutorial_active
		self.tutorial_menu_option.update_format("Yes" if self.tutorial_active else "No")
		
	def move_down(self):
		self.current_option = (self.current_option + 1) % self.num_options
		
	def move_up(self):
		self.current_option = (self.current_option - 1) % self.num_options	
		
	def select(self):
		self.options[self.current_option].func(self)
		
	def update(self):
		if not pyxel.frame_count % self.frame_gap:
			self.current_animated_col_index = (self.current_animated_col_index + 1) % len(self.animated_col_list)
			pyxel.pal(self.animated_col, self.animated_col_list[self.current_animated_col_index])
		
	def draw_before_children(self):
		pyxel.rect(*self.corner, *self.corner.br_of(self.size), self.bg_col)
		self.character_sprite.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.2))), Anchor.MIDDLE, Anchor.MIDDLE)
		self.title.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.4))), Anchor.MIDDLE, Anchor.MIDDLE)
		distance_down = 0.6
		seperator = 0.1
		for i, option in enumerate(self.options):
			option.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,distance_down + i*seperator))), Anchor.MIDDLE, Anchor.MIDDLE, self.selected_col if i == self.current_option else None)
		self.credit_text.draw(self.corner.br_of(Size(0, self.size.y)), Anchor.LEFT, Anchor.BOTTOM)	
		