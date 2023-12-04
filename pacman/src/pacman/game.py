from dataclasses import dataclass
from pacman.models.ghost import Ghost
from pacman.models.maze import Empty, Fruit, Maze
from pacman.models.pacman import PacMan


@dataclass
class GameState:
    score: int
    won: bool
    life: int
    maze: list[list[str]]

    @property
    def height(self) -> int:
        return len(self.maze)

    @property
    def width(self) -> int:
        return len(self.maze[0])


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

        self.check_colision()

    def check_colision(self):
        if self.pac_man.position in [ghost.position for ghost in self.ghosts]:
            self.life -= 1

    def move_ghosts(self) -> None:
        for ghost in self.ghosts:
            if self.maze.can_move(ghost.next_position):
                ghost.move()

    def move_pac_man(self):
        if not self.maze.can_move(self.pac_man.next_position):
            return

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

    def to_game_state(self) -> GameState:
        return GameState(
            score=self.score,
            life=self.life,
            maze=self.to_list(),
            won=self.won,
        )
