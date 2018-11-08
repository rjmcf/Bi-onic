from game_window import Root, TestChild
import pyxel

class App:
	def __init__(self):
		character_display_window = TestChild(0,0, 1,0.4, 3)
		control_bars = TestChild(0.9,0.1, 0.05,0.8, 14)
		character_display_window.child_windows = [control_bars]
		graph_area = TestChild(0,0.4, 1,0.6, 12)
		danger_high = TestChild(0,0, 1,0.5, 9)
		danger_low = TestChild(0,0.8, 1,0.2, 8)
		graph_area.child_windows = [danger_high, danger_low]
		self.root = Root(255,160,"TestWindow", [character_display_window, graph_area])	
		self.root.start()	

App()