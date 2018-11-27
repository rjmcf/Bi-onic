import pyxel
from plugins.geometry import Point, Proportion2D, Size
from plugins.window import Window
from plugins.sprite import Sprite, TextSprite

# Represents the possible options for the Main Menu
# Defines the methods that the logical and visual representations of the Main Menu must
# provide.
class MainMenuOptionHolder():
	def start_game(self):
		return self.start_game()
	def quit(self):
		return self.quit()
		
# Contains the logic for the Main Menu
#TODO Refactor: Possibly mix logic and representation here? The benefits of separation 
# may be outweighed by the complexity of trying to keep both in sync
class MainMenu(MainMenuOptionHolder):
	def __init__(self, start_game_interface):	
		self.options = [MainMenuOptionHolder.start_game, MainMenuOptionHolder.quit]
		self.num_options = len(self.options)
		self.current_option = 0
		self.start_game_interface = start_game_interface
		
	def set_display(self, display):
		self.display = display
		
	def move_down(self):
		self.current_option = (self.current_option + 1) % self.num_options
		self.display.set_current_option(self.current_option)
		
	def move_up(self):
		self.current_option = (self.current_option - 1) % self.num_options	
		self.display.set_current_option(self.current_option)
		
	def select(self):
		self.options[self.current_option](self)
		
	def start_game(self):
		self.start_game_interface.start_game()
		
	def quit(self):
		pyxel.quit()
		
# The visual representation of the Main Menu	
class MainMenuWindow(Window, MainMenuOptionHolder):
	def __init__(self, main_menu):
		super(MainMenuWindow, self).__init__(Point(0,0), Proportion2D(1,1))
		self.current_option = main_menu.current_option
		self.bg_col = 0
		self.text_col = 7
		self.selected_col = 8
		self.character_sprite = Sprite(Point(0,0), Size(32,40), 0, 0)
		self.get_options(main_menu.options)
		
	def get_options(self, func_list):	
		self.options = []
		for f in func_list:
			self.options.append(f(self))
		
	def set_current_option(self, current_option):
		self.current_option = current_option
		
	def draw_before_children(self):
		self.character_sprite.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,0.2))), True, True)
		distance_down = 0.5
		seperator = 0.1
		for i, option in enumerate(self.options):
			option.draw(self.corner.br_of(self.size.scale2D(Proportion2D(0.5,distance_down + i*seperator))), True, True, self.selected_col if i == self.current_option else None)
		
	def start_game(self):
		return TextSprite("Start Game", self.text_col)
		
	def quit(self):
		return TextSprite("Quit", self.text_col)
		
		
		
		