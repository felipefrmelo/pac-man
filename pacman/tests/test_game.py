from pacman.game import Game, Maze
from pacman.models.pacman import PacMan


def test_init_game():

    maze = Maze.from_str("""
    ......
    ......
    ......
    """)

    pac_man = PacMan((1, 1), maze)

    game = Game(maze, pac_man)

    assert game.score == 0
