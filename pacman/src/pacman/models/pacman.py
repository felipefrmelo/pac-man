
from typing import Protocol

from pacman.models.maze import Maze
from pacman.models.position import Position, Direction


class Subscriber(Protocol):

    def update(self, direction: Direction):
        ...


class PacMan(Subscriber):

    def __init__(self, position: tuple[int, int], maze: Maze) -> None:
        self.position = Position(*position)
        self.lives = 3
        self.direction = Direction.RIGHT
        self.maze = maze

    def move(self):

        new_position = self.position.get(self.direction)

        if self.maze.can_move(new_position):
            self.position = new_position

    def update(self, direction: Direction):
        self.direction = direction
