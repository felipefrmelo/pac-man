
from pacman.models.position import Position, Direction


class PacMan:

    def __init__(self, position: tuple[int, int] | Position) -> None:
        self.position = Position(*position)
        self.lives = 3
        self.direction = Direction.RIGHT

    def move(self):

        self.position = self.next_position

    def update(self, direction: Direction):
        self.direction = direction

    @property
    def next_position(self):
        return self.position.get(self.direction)

    def __str__(self):
        return 'p'
