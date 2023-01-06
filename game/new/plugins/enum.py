class Enum():
    def __init__(self, value : int) -> None:
        self.value = value

    def __eq__(self, other : object) -> bool:
        # first part allows accessing `value`, second checks for exact types
        if isinstance(other, Enum) and type(self) == type(other):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented
