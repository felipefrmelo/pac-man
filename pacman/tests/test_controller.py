import pytest
from pacman.game import Game, Maze, PacMan
from pacman.controller import Controller, GameState
from pacman.models.position import Direction, Position


class FakeInput:

    subscriber: PacMan

    def __init__(self, subscriber: PacMan) -> None:
        self.subscriber = subscriber

    def dispatch(self, direction: Direction) -> None:
        self.subscriber.update(direction)


class FakeTimer:

    _count: int

    def __init__(self, max_count: int = 1) -> None:
        self._max_count = max_count
        self._count = 0

    def sleep(self, milliseconds: int) -> None:

        if self._count >= self._max_count:
            self._count = 0
            raise KeyboardInterrupt

        self._count += 1


class FakePresenter:

    is_called_with: GameState | None

    def __init__(self) -> None:
        self.is_called_with = None

    def present(self, game_state: GameState) -> None:
        self.is_called_with = game_state


@pytest.fixture
def game():

    maze = Maze.from_str("""
    wwwwww
    w....w
    w.f..w
    w....w
    wwwwww
    """)
    pac_man = PacMan(Position(1, 1))

    return Game(maze, pac_man)


@pytest.fixture
def presenter():

    return FakePresenter()


@pytest.fixture
def controller(game: Game, presenter: FakePresenter):

    return Controller(game, FakeTimer(1), presenter)


def test_run_one_game_frames(game: Game, controller: Controller):

    with pytest.raises(KeyboardInterrupt):
        controller.run()

    assert game.pac_man.position == Position(1, 2)
    assert game.score == 0
    assert game.won is False


def test_won_game_when_eat_the_fruit(game: Game, controller: Controller):

    fake_input = FakeInput(game.pac_man)

    with pytest.raises(KeyboardInterrupt):
        controller.run()

    fake_input.dispatch(Direction.DOWN)

    controller.run()

    assert game.won is True


def test_presentation_is_called_correcty(controller: Controller):

    controller.presenter = FakePresenter()

    with pytest.raises(KeyboardInterrupt):
        controller.run()

    expected = GameState(score=0, won=False, maze=[['w', 'w', 'w', 'w', 'w', 'w'],
                                                   ['w', '.', 'p', '.', '.', 'w'],
                                                   ['w', '.', 'f', '.', '.', 'w'],
                                                   ['w', '.', '.', '.', '.', 'w'],
                                                   ['w', 'w', 'w', 'w', 'w', 'w']])

    assert controller.presenter.is_called_with == expected
