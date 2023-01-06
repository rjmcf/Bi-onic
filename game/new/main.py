import pyxel

class App:
    def __init__(self) -> None:
        pyxel.init(255,160)
        pyxel.load("assets/bionic_resources.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.cls(0)
        
App()

# use the following console command to type check
# mypy main.py --namespace-packages  