from pacman.game import Game, Maze
from pacman.models.pacman import PacMan


def test_init_game():

    maze = Maze([['wall', 'wall', 'wall', 'wall'],
                ['wall', 'empty', 'empty', 'wall'],
                ['wall', 'empty', 'empty', 'wall'],
                ['wall', 'wall', 'wall', 'wall']
                 ])

    pac_man = PacMan((1, 1))

    game = Game(maze, pac_man)

    assert game.score == 0
