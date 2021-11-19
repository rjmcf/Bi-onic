from core import Core

class App:
	def __init__(self):
		self.core = Core()
		self.core.start()	

App()

# use the following console command to type check
# mypy bi-onic.py --namespace-packages --ignore-missing-imports
