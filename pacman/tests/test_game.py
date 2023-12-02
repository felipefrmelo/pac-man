import pytest
from pacman.game import Game
from pacman.models.maze import Empty, Maze
from pacman.models.pacman import PacMan
from pacman.models.position import Direction, Position


@pytest.fixture
def pac_man():
    result = PacMan((1, 1))
    result.update(Direction.RIGHT)
    return result


def run_game_frames(game: Game, n: int):
    for _ in range(n):
        game.next_frame()


def test_init_game(pac_man: PacMan):

    maze = Maze.from_str("""
    ......
    ..f...
    ......
    """)

    game = Game(maze, pac_man)

    assert game.score == 0
    assert game.won is False


def test_run_one_frame(pac_man: PacMan):

    maze = Maze.from_str("""
                ......
                ......
                ......
            """)

    game = Game(maze, pac_man)

    game.next_frame()

    assert game.score == 0
    assert pac_man.position == Position(1, 2)


def test_pacman_does_not_move_if_wall_in_front(pac_man: PacMan):

    maze = Maze.from_str("""
                wwwww
                w...w
                w...w
                w...w
                wwwww
            """)

    game = Game(maze, pac_man)

    run_game_frames(game, 3)

    assert game.pac_man.position == Position(1, 3)

    pac_man.update(Direction.DOWN)

    run_game_frames(game, 5)

    assert game.pac_man.position == Position(3, 3)


def test_pacman_can_eat_a_fruit(pac_man: PacMan):

    maze = Maze.from_str("""
        wwwwww
        w..f.w
        w....w
        w....w
        wwwwww
    """)

    game = Game(maze, pac_man)

    run_game_frames(game, 2)

    assert game.score > 0
    assert game.maze.get_cell(pac_man.position) == Empty()


def test_pacman_can_eat_many_fruits(pac_man: PacMan):

    maze = Maze.from_str("""
        wwwwww
        w..f.w
        w.ff.w
        w....w
        wwwwww
    """)

    game = Game(maze, pac_man)

    run_game_frames(game, 2)

    pac_man.update(Direction.DOWN)

    run_game_frames(game, 1)

    assert game.maze.get_cell(Position(1, 3)) == Empty()
    assert game.maze.get_cell(Position(2, 3)) == Empty()
    assert game.score > 0


def test_pacman_wins_if_eats_all_the_fruits(pac_man: PacMan):

    maze = Maze.from_str("""
        wwwwww
        w..f.w
        w.ff.w
        w....w
        wwwwww
    """)

    game = Game(maze, pac_man)

    run_game_frames(game, 2)

    pac_man.update(Direction.DOWN)

    run_game_frames(game, 1)

    pac_man.update(Direction.LEFT)

    run_game_frames(game, 1)

    assert game.won
