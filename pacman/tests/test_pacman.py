import pytest
from pacman.models.pacman import Direction, PacMan
from pacman.models.maze import Maze


@pytest.fixture
def pac_man():

    maze = Maze.from_str("""
    ......
    ......
    ......
    ......
    ......
    """)
    return PacMan((1, 1), maze)


def test_init_pacman(pac_man: PacMan):

    assert pac_man.lives == 3
    assert pac_man.direction == Direction.RIGHT
    assert pac_man.position == (1, 1)


def test_pacman_move_right(pac_man: PacMan):

    pac_man.move()

    assert pac_man.position == (1, 2)

    pac_man.move()

    assert pac_man.position == (1, 3)


@pytest.mark.parametrize('direction', [
    Direction.RIGHT,
    Direction.LEFT,
    Direction.UP,
    Direction.DOWN
])
def test_pacman_change(pac_man: PacMan, direction: Direction):
    pac_man.update(direction)
    assert pac_man.direction == direction


@pytest.mark.parametrize('direction,  expected_position', [
    (Direction.RIGHT, (1, 2)),
    (Direction.LEFT, (1, 0)),
    (Direction.UP, (0, 1)),
    (Direction.DOWN, (2, 1))
])
def test_pacman_move(pac_man: PacMan, direction: Direction, expected_position):
    pac_man.update(direction)

    pac_man.move()

    assert pac_man.position == expected_position


def test_pacman_does_not_move_to_wall():
    maze = Maze.from_str("""
                     www
                     w.w
                     www
                """)
    pac_man = PacMan((1, 1), maze)

    pac_man.move()

    assert pac_man.position == (1, 1)
