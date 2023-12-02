from pynput import keyboard

from pacman.controller import Controller, GameState
from pacman.game import Game
from pacman.models.maze import Maze
from pacman.models.pacman import PacMan
from pacman.models.position import Direction
import time
import os


class ListenerInput:
    def __init__(self, pac_man: PacMan) -> None:
        self.pac_man = pac_man

    def on_press(self, key):
        try:
            direction = self.get_direction(key)
            if direction:
                self.pac_man.update(direction)

        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def get_direction(self, key):
        keys_map = {
            keyboard.Key.up: Direction.UP,
            keyboard.Key.down: Direction.DOWN,
            keyboard.Key.left: Direction.LEFT,
            keyboard.Key.right: Direction.RIGHT,
        }
        direction = keys_map.get(key)
        return direction

    def start(self):
        keyboard.Listener(on_press=self.on_press).start()


class PresenterCli:

    def present(self, game_state: GameState) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        # get size of terminal
        size = os.get_terminal_size()

        print("\n" * min((size.lines - game_state.height) // 2, 10), end="")
        left_padding = (size.columns - game_state.width) // 2
        print(" " * left_padding, end="")
        print("Score: ", game_state.score)
        for row in game_state.maze:
            print(" " * left_padding, end="")
            print("".join(row))
        print("\n" * ((size.lines - game_state.height) // 2), end="")
        print(" " * left_padding, end="")


class TimerAdapter:

    def sleep(self, milliseconds: int) -> None:
        time.sleep(milliseconds/1000)


def main():
    pac_man = PacMan((1, 1))

    maze = Maze.from_str("""
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        wf....w...w...w...w...w...w...w...w...w...w...w...w...w...w...w...w....fw
        wwww.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.ww
        w...........f......................................................f...ww
        wwwwww.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.ww
        w...................................f...................................w
        wwww.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.ww
        w................f......................................................w
        wwww.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.w.ww
        w......................................................................ww
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    """)

    game = Game(maze, pac_man)

    controller = Controller(game, TimerAdapter(), PresenterCli())

    listenerInput = ListenerInput(pac_man)

    listenerInput.start()

    controller.run()


if __name__ == '__main__':
    main()
