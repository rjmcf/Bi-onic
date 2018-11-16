class GameState():
	def __init__(self, threat_display_interface):
		self.player_threat_percent = 0
		self.threat_display_interface = threat_display_interface
		
	def update(self):
		self.threat_display_interface.set_threat_percentage(self.player_threat_percent)
		
	def set_player_threat_percent(self, threat_percent):
		self.player_threat_percent = min(1, max(0, threat_percent))
		
class ThreatInterface():
	def __init__(self, game_state):
		self.game_state = game_state
		
	def adjust_threat_percent(self, threat_adjustment):
		self.game_state.set_player_threat_percent(self.game_state.player_threat_percent + threat_adjustment)