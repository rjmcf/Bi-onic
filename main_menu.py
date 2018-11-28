import pyxel
from plugins.geometry import Point, Proportion2D, Size
from plugins.window import Window
from plugins.sprite import Sprite, TextSprite

class MainMenuOption(TextSprite):
	def __init__(self, text, col, func):
		super(MainMenuOption, self).__init__(text, col)
		self.func = func
		
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
		self.options = [
			MainMenuOption("Start Game", self.text_col, lambda main_menu: main_menu.start_game_interface.start_game()),
			MainMenuOption("Quit", self.text_col, lambda main_menu: pyxel.quit())
		]	
		self.num_options = len(self.options)
		self.current_option = 0
		self.credit_text = TextSprite("By Robin McFarland: @RjmcfDev", 7)
		self.title = Sprite(Point(0,96), Size(67,18), 0, 0)
		
	def move_down(self):
		self.current_option = (self.current_option + 1) % self.num_options
		
	def move_up(self):
		self.current_option = (self.current_option - 1) % self.num_options	
		
	def select(self):
		self.options[self.current_option].func(self)
		
	def draw_before_children(self):
		pyxel.rect(*self.corner, *self.corner.br_of(self.size), self.bg_col)
		self.character_sprite.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.2))), True, True)
		self.title.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.4))), True, True)
		distance_down = 0.6
		seperator = 0.1
		for i, option in enumerate(self.options):
			option.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,distance_down + i*seperator))), True, True, self.selected_col if i == self.current_option else None)
		self.credit_text.draw(self.corner.br_of(Size(0, self.size.y * 0.95)))	
		