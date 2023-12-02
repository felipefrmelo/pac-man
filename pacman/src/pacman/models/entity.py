
from pacman.models.position import Position, Direction


class MazeChar:

    def __init__(self, position: tuple[int, int] | Position, direction=Direction.RIGHT) -> None:
        self.position = Position(*position)
        self.direction = direction

    def move(self):
        self.position = self.next_position

    def update(self, direction: Direction):
        self.direction = direction

    @property
    def next_position(self):
        return self.position.get(self.direction)

    def __str__(self):
        return self.__class__.__name__[0].lower()
