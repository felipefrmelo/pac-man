from dataclasses import dataclass

from pacman.models.position import Position


@dataclass
class Cell:
    pass


class Wall(Cell):

    pass


class Fruit(Cell):
    pass


class Empty(Cell):
    pass


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
        row, col = position
        return self.cells[row][col] != Wall()
