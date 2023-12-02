from pacman.models.maze import Empty, Fruit, Maze
from pacman.models.pacman import PacMan


class Game:

    def __init__(self, maze: Maze, pac_man: PacMan) -> None:
        self.score = 0
        self.maze = maze
        self.pac_man = pac_man

    def next_frame(self) -> None:

        if self.maze.can_move(self.pac_man.next_position):
            self.pac_man.move()
            current_cell = self.maze.get_cell(self.pac_man.position)

            if current_cell == Fruit():
                self.maze.update(self.pac_man.position, Empty())

                self.score += 1

    @property
    def won(self) -> bool:
        return self.maze.no_fruits_left

    def to_list(self) -> list[list[str]]:
        result = [[str(cell) for cell in row] for row in self.maze.cells]
        row, col = self.pac_man.position

        result[row][col] = str(self.pac_man)
        return result
