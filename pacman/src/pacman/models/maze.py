from dataclasses import dataclass

from pacman.models.position import Position


@dataclass
class Cell:

    def __eq__(self, other):
        return isinstance(self, other.__class__)


class Wall(Cell):

    def __str__(self):
        return 'w'


class Fruit(Cell):

    def __str__(self):
        return 'f'


class Empty(Cell):
    def __str__(self):
        return '.'


class Maze:

    _cell_map = {
        "w": Wall,
        ".": Empty,
        "f": Fruit,
    }

    def __init__(self, cells: list[list[Cell]] = [[]]) -> None:
        self.cells = cells

    @property
    def shape(self):
        return (0, 0) if len(self.cells[0]) == 0 else (len(self.cells), len(self.cells[0]))

    @classmethod
    def from_str(cls, string: str):

        lines = string.strip().splitlines()

        cells = [[cls._get_cell(char) for char in line.strip()]
                 for line in lines]

        return cls(cells)

    @staticmethod
    def _get_cell(char: str) -> Cell:
        return Maze._cell_map[char]()

    def can_move(self, position: Position) -> bool:
        return self.get_cell(position) != Wall()

    def get_cell(self, position: Position) -> Cell:
        row, col = position
        return self.cells[row][col]

    def update(self, position: Position, cell: Cell):
        row, col = position
        self.cells[row][col] = cell

    @property
    def no_fruits_left(self):
        return len([cell for row in self.cells for cell in row if isinstance(cell, Fruit)]) == 0
