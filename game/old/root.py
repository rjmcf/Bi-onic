import pyxel
from plugins.window import TopLevelWindow, Window
from plugins.geometry import Size, Point
from plugins.sprite import TextSprite
from palette_settings import PALETTE
from graph import GraphWindow
from character_display import CharacterDisplay
from resource_settings import RESOURCE
from debug import ImageViewer, Tiler, PaletteViewer, GraphImager, TextImager
from typing import Any

# Determines whether we will allow DEBUG screens to be shown
DEBUG = True

# Represents the parent window that contains all the others. Controls switching of windows
# for debug and menu purposes.
# Makes sure that all child windows get told to draw at the right time
class Root(TopLevelWindow):
	def __init__(self, game_state : Any, main_menu : Any) -> None:
		super(Root, self).__init__(Size(255,160))
		self.palette = PALETTE
		self.game_state = game_state
		# This line needs to come before any Pyxel imports are used, otherwise they can't
		# be imported
		pyxel.init(*self.size)
		pyxel.load(RESOURCE)
		self.character_display_window = CharacterDisplay()
		self.graph_area = GraphWindow(Point(0,0), self.size)
		self.restart_text = TextSprite("Press R to Restart", 7)
		self.paused_text = TextSprite("Paused...", 7)
		self.game_windows = [self.character_display_window, self.graph_area]
		self.main_menu_windows = [main_menu]
		if DEBUG:
			self.debug_windows = [ImageViewer(self.palette), Tiler(), PaletteViewer(), GraphImager(), TextImager()]
			if len(self.debug_windows) != len(set(self.debug_windows)):
				print("debug windows with duplicate keys detected")
				quit()

	def toggle_debug_window(self, window : Any) -> None:
		if window not in self.windows:
			self.previous_windows = self.windows
			self.windows = [window]
		else:
			self.windows = self.previous_windows			

	def switch_to_game(self) -> None:
		self.windows = self.game_windows

	def switch_to_main_menu(self) -> None:
		self.windows = self.main_menu_windows

	def set_player_threat_display(self, player_threat : Any) -> None:
		self.character_display_window.set_player_threat_display(player_threat)

	def set_line_display(self, line : Any) -> None:
		self.graph_area.set_line_display(line)

	def set_character_display_reservoir_interface(self, controller : Any) -> None:
		self.character_display_window.set_character_display_reservoir_interface(controller)

	def set_character_display_control_interface(self, player_controller : Any) -> None:
		self.character_display_window.set_character_display_control_interface(player_controller)

	def set_character_display_text_interface(self, environment : Any) -> None:
		self.character_display_window.set_character_display_text_interface(environment)

	def set_score_display(self, score_display : Any) -> None:
		self.character_display_window.set_score_display(score_display)

	def reset(self) -> None:
		for thing in [self.character_display_window]:
			thing.reset()

	def update(self) -> None:
		super(Root, self).update()
		if DEBUG:
			for debug_window in self.debug_windows:
				if pyxel.btnp(debug_window.toggle_key):
					self.toggle_debug_window(debug_window)

	def draw(self) -> None:
		pyxel.cls(0)
		super(Root, self).draw()

		if self.game_state.in_game_mode():
			if not self.game_state.is_game_playing():
				self.restart_text.draw(Point(0,0))
			elif self.game_state.paused:
				self.paused_text.draw(Point(0,0))
