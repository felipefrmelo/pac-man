
from typing import Protocol
from enum import Enum, auto


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


class Subscriber(Protocol):

    def update(self, direction: Direction):
        ...


class PacMan(Subscriber):

    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position
        self.lives = 3
        self.direction = Direction.RIGHT

    def move(self):

        self._moves[self.direction]()

    @property
    def _moves(self):
        return {
            Direction.RIGHT: self.move_right,
            Direction.LEFT: self.move_left,
            Direction.UP: self.move_up,
            Direction.DOWN: self.move_down
        }

    def move_right(self):
        row, col = self.position
        self.position = (row, col + 1)

    def move_left(self):
        row, col = self.position
        self.position = (row, col - 1)

    def move_up(self):
        row, col = self.position
        self.position = (row - 1, col)

    def move_down(self):
        row, col = self.position
        self.position = (row + 1, col)

    def update(self, direction: Direction):
        self.direction = direction
