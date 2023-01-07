import pyxel
from windows import Window

class App:
    def __init__(self) -> None:
        pyxel.init(256,160)
        pyxel.load("assets/bionic_resources.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.cls(0)

        for window in Window.get_windows():
            window.draw()
        
App()

# use the following console command to type check
# mypy main.py --namespace-packages  