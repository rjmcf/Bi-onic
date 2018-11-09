import pyxel
from game_window import Root, TestChild, GraphWindow

class App:
	def __init__(self):
		self.root = Root(255,160,"Bi-onic")	
		self.root.start()	

App()