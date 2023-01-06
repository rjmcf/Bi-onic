class Point():
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y

    def __sub__(self, other : 'Point') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def displace(self, vector : 'Vector') -> 'Point':
        return Point(self.x + vector.x, self.y + vector.y)

class Vector():
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y

    def scale(self, multiplier : float) -> 'Vector':
        return Vector(self.x * multiplier, self.y * multiplier)
        
    def magnitude2(self) -> float:
        return self.x**2 + self.y**2