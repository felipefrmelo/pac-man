import pytest
from pacman.models.pacman import PacMan
from pacman.models.position import Position, Direction


@pytest.fixture
def pac_man():

    return PacMan((1, 1))


def test_init_pacman(pac_man: PacMan):

    assert pac_man.direction == Direction.RIGHT
    assert pac_man.position == Position(1, 1)


def test_pacman_move_right(pac_man: PacMan):

    initial_position = pac_man.position

    pac_man.move()

    assert pac_man.position == initial_position.right

    pac_man.move()

    assert pac_man.position == initial_position.right.right


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

    assert pac_man.position == Position(*expected_position)
