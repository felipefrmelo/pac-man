
from typing import Protocol
from enum import Enum, auto

from pacman.models.maze import Maze


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


class Subscriber(Protocol):

    def update(self, direction: Direction):
        ...


class PacMan(Subscriber):

    def __init__(self, position: tuple[int, int], maze: Maze) -> None:
        self.position = position
        self.lives = 3
        self.direction = Direction.RIGHT
        self.maze = maze

    def move(self):

        new_position = self._moves[self.direction]()

        if self.maze.can_move(new_position):
            self.position = new_position

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
        return (row, col + 1)

    def move_left(self):
        row, col = self.position
        return (row, col - 1)

    def move_up(self):
        row, col = self.position
        return (row - 1, col)

    def move_down(self):
        row, col = self.position
        return (row + 1, col)

    def update(self, direction: Direction):
        self.direction = direction
