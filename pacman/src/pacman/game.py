
from pacman.models.maze import Maze
from pacman.models.pacman import PacMan


class Game:

    def __init__(self, maze: Maze, pacman: PacMan) -> None:
        self.score = 0
        self.maze = maze
        self.pacman = pacman

    def run_one_frame(self) -> None:

        self.pacman.position = (1, 2)
