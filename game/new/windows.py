import pyxel
from typing import List

class Window():
    def __init__(self, x : int, y : int, w : int, h : int, colour : int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour

    def draw(self) -> None:
        pyxel.rect(self.x, self.y, self.w, self.h, self.colour)

    @staticmethod
    def get_windows() -> List['Window']:
        # Specified in order they must be drawn
        return [ 
            Window(  0, 0, 128,80, 1),
            Window(128, 0, 128,80, 2),
            Window(  0,80, 128,80, 3),
            Window(128,80, 128,80, 4),
            Window( 64,40, 128,80, 5)
        ] 
