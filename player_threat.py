from plugins.window import Window
from bars import FillableBar

class PlayerThreat():
	def __init__(self, game_state):
		self.player_threat_percent = 0
		self.game_state = game_state
		
	def set_display(self, display):
		self.display = display
		
	def set_player_threat_percent(self, threat_percent):
		self.player_threat_percent = min(1, max(0, threat_percent))
		self.display.set_player_threat_percent(self.player_threat_percent)
		
	def update(self):
		if self.player_threat_percent == 1:
			self.game_state.game_playing = False
			
	def reset(self):
		self.set_player_threat_percent(0)

class PlayerThreatWindow(Window):
	def __init__(self, x_prop, y_prop, width_prop, height_prop, background_col, border_col):
		super(PlayerThreatWindow, self).__init__(x_prop, y_prop, width_prop, height_prop)
		
		self.background_col = background_col
		self.foreground_col = 8
		self.border_col = border_col
		
		self.player_threat_display = FillableBar(0,0, 1,1, True,False, self.background_col,self.foreground_col, self.border_col)
		self.child_windows = [self.player_threat_display]
		
	def set_player_threat_percent(self, threat_percent):
		self.player_threat_display.set_bar(threat_percent)
		
class PlayerThreatInterface():
	def __init__(self, player_threat):
		self.player_threat = player_threat
		
	def adjust_threat_percent(self, threat_adjustment):
		self.player_threat.set_player_threat_percent(self.player_threat.player_threat_percent + threat_adjustment)