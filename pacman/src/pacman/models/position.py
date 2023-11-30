
from dataclasses import dataclass
from enum import Enum, auto


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class Position:
    row: int
    col: int

    @property
    def up(self):
        return Position(self.row - 1, self.col)

    @property
    def down(self):
        return Position(self.row + 1, self.col)

    @property
    def left(self):
        return Position(self.row, self.col - 1)

    @property
    def right(self):
        return Position(self.row, self.col + 1)

    def get(self, direction: Direction):
        return {
            Direction.RIGHT: self.right,
            Direction.LEFT: self.left,
            Direction.UP: self.up,
            Direction.DOWN: self.down
        }[direction]

    def __eq__(self, other):

        return self.row == other.row and self.col == other.col

    def __iter__(self):
        yield self.row
        yield self.col
