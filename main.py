from game_window import Root, TestChild, GraphWindow
import pyxel

class App:
	def __init__(self):
		self.root = Root(255,160,"Bi-onic")	
		self.root.start()	

App()