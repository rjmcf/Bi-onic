import pyxel
from core import Core

class App:
	def __init__(self):
		self.core = Core()
		self.core.start()	

App()