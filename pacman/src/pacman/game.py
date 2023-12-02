from pacman.models.ghost import Ghost
from pacman.models.maze import Empty, Fruit, Maze
from pacman.models.pacman import PacMan


class Game:

    def __init__(self, maze: Maze, pac_man: PacMan, ghosts: list[Ghost] = []) -> None:
        self.score = 0
        self.life = 3
        self.maze = maze
        self.pac_man = pac_man
        self.ghosts = ghosts

    def next_frame(self) -> None:
        if self.won or self.life == 0:
            return

        self.move_pac_man()
        self.move_ghosts()

        for ghost in self.ghosts:
            if ghost.position == self.pac_man.position:
                self.life -= 1
                break

    def move_ghosts(self) -> None:
        for ghost in self.ghosts:
            if self.maze.can_move(ghost.next_position):
                ghost.move()

    def move_pac_man(self):
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
        for ghost in self.ghosts:
            row, col = ghost.position
            result[row][col] = str(ghost)
        return result
