
from pacman.models.entity import MazeChar


class Ghost(MazeChar):
    pass


class Pinky(Ghost):

    def __str__(self):
        return 't'


class Inky(Ghost):
    pass


class Blinky(Ghost):
    pass


class Clyde(Ghost):
    pass


def new_ghosts(position: tuple[int, int]) -> list[Ghost]:
    return [Blinky(position), Pinky(position),
            Inky(position), Clyde(position)]
