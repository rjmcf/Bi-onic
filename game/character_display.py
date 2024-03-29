import pyxel
from plugins.window import Window
from plugins.geometry import Proportion2D, Vector
from plugins.sprite import Anchor, TextSprite
from bars import FillableBar
from player_controller import DownAffector
from player_threat import PlayerThreatWindow
from score_keeper import ScoreDisplayWindow
from typing import Any

# The window that shows the 'HUD' elements, including:
# 	Control UI
#	Threat UI
#	Text descriptions of active events
# TODO Unfinished: Show Character state
class CharacterDisplay(Window):
	def __init__(self) -> None:
		super(CharacterDisplay, self).__init__(Proportion2D(0,0), Proportion2D(1,0.4))
		self.background = 1
		self.control_border = 7
		self.up_control = FillableBar(Proportion2D(0.9,0.1), Proportion2D(0.05,0.4), True,False, self.background,14, self.control_border)
		self.down_control = FillableBar(Proportion2D(0.9,0.5), Proportion2D(0.05,0.4), True,True, self.background,3, self.control_border)
		self.down_reservoir = FillableBar(Proportion2D(0.85,0.5), Proportion2D(0.05,0.4), True,False, self.background,3, self.control_border)
		self.player_threat_display = PlayerThreatWindow(Proportion2D(0.05,0.1), Proportion2D(0.05,0.8), self.background, self.control_border)
		self.score_display = ScoreDisplayWindow()
		# Maintain mapping of active sprites to the amount of time we should display them for
		self.active_text_sprites : dict[TextSprite, int] = {}
		self.child_windows = [self.up_control, self.down_control, self.down_reservoir, self.player_threat_display, self.score_display]

	def set_character_display_reservoir_interface(self, controller : Any) -> None:
		controller.set_character_display_reservoir_interface(CharacterDisplayReservoirInterface(self))

	def set_character_display_control_interface(self, player_controller : Any) -> None:
		player_controller.set_character_display_control_interface(CharacterDisplayControlInterface(self))

	def set_character_display_text_interface(self, environment : Any) -> None:
		environment.set_character_display_text_interface(CharacterDisplayTextInterface(self))

	def set_score_display(self, score_keeper : Any) -> None:
		score_keeper.set_display(self.score_display)

	def reset(self) -> None:
		self.up_control.set_bar(0)
		self.down_control.set_bar(0)
		self.down_reservoir.set_bar(0)
		self.active_text_sprites = {}

		self.score_display.reset()

	def empty_down_reservoir(self) -> None:
		self.down_reservoir.set_bar(0)

	def add_down_reservoir_amount(self, percent_increase : float) -> None:
		self.down_reservoir.adjust_bar(percent_increase)

	def set_player_threat_display(self, player_threat : Any) -> None:
		player_threat.set_display(self.player_threat_display)

	def add_text(self, text_sprite : TextSprite, duration : int) -> None:
		self.active_text_sprites[text_sprite] = duration

	def update(self) -> None:
		for text_sprite in list(self.active_text_sprites.keys()):
			self.active_text_sprites[text_sprite] -= 1
			if self.active_text_sprites[text_sprite] == 0:
				del self.active_text_sprites[text_sprite]

	def draw_before_children(self) -> None:
		pyxel.rect(*self.corner, *self.size, self.background)
		for text_sprite in self.active_text_sprites:
			text_sprite.draw(self.corner.translate(Vector(*self.size.scale2D(Proportion2D(0.5,0.5)))), Anchor(Anchor.MIDDLE), Anchor(Anchor.MIDDLE))

# Interface for player_controller to use the control UI
class CharacterDisplayControlInterface():
	def __init__(self, character_display : Any) -> None:
		self.character_display = character_display

	def set_up_control(self, percent : float) -> None:
		self.character_display.up_control.set_bar(percent)

	def set_down_control(self, percent : float) -> None:
		self.character_display.down_control.set_bar(percent)

# Interface for controller to use the reservoir UI
class CharacterDisplayReservoirInterface():
	def __init__(self, character_display : Any) -> None:
		self.character_display = character_display

	def empty_down_reservoir(self) -> None:
		self.character_display.empty_down_reservoir()

	def add_down_reservoir_amount(self, amount : float) -> None:
		self.character_display.add_down_reservoir_amount(amount)

# Interface for the environment to display descriptions of active events
class CharacterDisplayTextInterface():
	def __init__(self, character_display : Any) -> None:
		self.character_display = character_display

	def add_text(self, text_sprite : TextSprite, duration : int) -> None:
		self.character_display.add_text(text_sprite, duration)

# Interface for environment to use Threat UI
class ThreatDisplayInterface():
	def __init__(self, character_display : Any) -> None:
		self.character_display = character_display

	def set_threat_percentage(self, threat_percentage : float) -> None:
		self.character_display.set_threat_percentage(threat_percentage)
