import pytest
from pacman.game import Game
from pacman.models.maze import Empty, Maze
from pacman.models.pacman import PacMan
from pacman.models.position import Direction, Position
from pacman.models.ghost import Ghost, Pinky, Blinky, Inky, Clyde


@pytest.fixture
def pac_man():
    result = PacMan((1, 1))
    result.update(Direction.RIGHT)
    return result


def run_game_frames(game: Game, n: int):
    for _ in range(n):
        game.next_frame()


def make_game(pac_man, maze_str, ghosts=[]):
    maze = Maze.from_str(maze_str)

    return Game(maze, pac_man, ghosts=ghosts)


def make_ghosts(position: Position | tuple[int, int]) -> list[Ghost]:
    return [Blinky(position), Pinky(position),
            Inky(position), Clyde(position)]


def test_init_game(pac_man: PacMan):

    game = make_game(pac_man, """
    ......
    ..f...
    ......
    """)

    assert game.score == 0
    assert game.won is False
    assert game.life == 3


def test_run_one_frame(pac_man: PacMan):

    game = make_game(pac_man, """
                ......
                ....f.
                ......
            """)

    game.next_frame()

    assert game.score == 0
    assert pac_man.position == Position(1, 2)


def test_pacman_does_not_move_if_wall_in_front(pac_man: PacMan):

    game = make_game(pac_man, """
                wwwww
                w...w
                w.f.w
                w...w
                wwwww
            """)

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

    game = make_game(pac_man,
                     """ 
                            wwwwww 
                            w..f.w 
                            w.ff.w 
                            w....w 
                            wwwwww 
                        """
                     )

    run_game_frames(game, 2)

    pac_man.update(Direction.DOWN)

    run_game_frames(game, 1)

    assert game.maze.get_cell(Position(1, 3)) == Empty()
    assert game.maze.get_cell(Position(2, 3)) == Empty()
    assert game.score > 0


def test_pacman_wins_if_eats_all_the_fruits(pac_man: PacMan):

    game = make_game(pac_man,
                     """ 
                            wwwwww 
                            w..f.w 
                            w.ff.w 
                            w....w 
                            wwwwww 
                        """
                     )

    run_game_frames(game, 2)

    pac_man.update(Direction.DOWN)

    run_game_frames(game, 1)

    pac_man.update(Direction.LEFT)

    run_game_frames(game, 1)

    assert game.won


def test_pacman_is_in_the_list(pac_man: PacMan):

    game = make_game(pac_man,
                     """ 
                        wwwwww 
                        w..f.w 
                        w.ff.w 
                        w....w 
                        wwwwww 
                    """
                     )

    assert game.to_list() == [
        ['w', 'w', 'w', 'w', 'w', 'w'],
        ['w', 'p', '.', 'f', '.', 'w'],
        ['w', '.', 'f', 'f', '.', 'w'],
        ['w', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w']
    ]


def test_ghost_moves(pac_man: PacMan):

    ghosts = make_ghosts(Position(1, 4))

    game = make_game(pac_man, maze_str="""
        wwwwww
        w....w
        w....w
        w.f..w
        w....w
        wwwwww
    """, ghosts=ghosts)

    update_ghost_direction(ghosts)

    run_game_frames(game, 1)

    for ghost in ghosts:
        assert ghost.position == Position(2, 4)


def test_ghost_does_not_move_if_wall_in_front(pac_man: PacMan):

    ghosts = make_ghosts(Position(1, 4))

    game = make_game(pac_man, maze_str="""
        wwwwww
        w....w
        w.f..w
        w....w
        w....w
        wwwwww
    """, ghosts=ghosts)

    update_ghost_direction(ghosts)

    run_game_frames(game, 5)

    for ghost in ghosts:
        assert ghost.position == Position(4, 4)


def update_ghost_direction(ghosts, direction=Direction.DOWN):
    for ghost in ghosts:
        ghost.update(direction)


def test_ghosts_are_in_the_list(pac_man: PacMan):

    ghosts = make_ghosts(Position(3, 3))

    for (ghost, direction) in zip(ghosts, [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]):
        ghost.update(direction)

    game = make_game(pac_man, maze_str="""
        wwwwww
        w....w
        w.f..w
        w....w
        w....w
        wwwwww
    """, ghosts=ghosts)

    run_game_frames(game, 1)

    assert game.to_list() == [
        ['w', 'w', 'w', 'w', 'w', 'w'],
        ['w', '.', 'p', '.', '.', 'w'],
        ['w', '.', 'f', 'i', '.', 'w'],
        ['w', '.', 't', '.', 'b', 'w'],
        ['w', '.', '.', 'c', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w']
    ]


def test_pacman_die_if_is_in_the_same_postion_as_a_ghost(pac_man: PacMan):

    ghosts = make_ghosts(Position(1, 4))

    game = make_game(pac_man, maze_str="""
        wwwwww
        w....w
        w....w
        w..f.w
        w....w
        wwwwww
    """, ghosts=ghosts)

    update_ghost_direction(ghosts, Direction.RIGHT)

    run_game_frames(game, 3)

    assert game.life == 2


def test_game_lost_when_pacman_die_3_times(pac_man: PacMan):

    ghosts = make_ghosts(Position(1, 4))

    game = make_game(pac_man, maze_str="""
        wwwwww
        w....w
        w....w
        w....w
        w..f.w
        wwwwww
    """, ghosts=ghosts)

    update_ghost_direction(ghosts, Direction.RIGHT)

    run_game_frames(game, 9)

    assert game.life == 0
    assert game.won is False
