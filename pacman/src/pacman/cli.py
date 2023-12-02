from pynput import keyboard

from pacman.controller import Controller, GameState
from pacman.game import Game
from pacman.models.entity import MazeChar
from pacman.models.ghost import new_ghosts
from pacman.models.maze import Maze
from pacman.models.pacman import PacMan
from pacman.models.position import Direction
import time
import random
import os
import threading


class ListenerInput:
    def __init__(self, maze_char: MazeChar) -> None:
        self.pac_man = maze_char

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


class RandomInput:

    def __init__(self, maze_char: MazeChar) -> None:
        self.maze_char = maze_char

    def start(self):
        threading.Thread(target=self.randon_choice).start()

    def randon_choice(self):
        while True:
            time.sleep(0.8)
            direction = random.choice(list(Direction))
            self.maze_char.update(direction)


class PresenterCli:

    def present(self, game_state: GameState) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        size = os.get_terminal_size()

        print("\n" * min((size.lines - game_state.height) // 2, 10), end="")
        left_padding = (size.columns - game_state.width) // 2
        print(" " * left_padding, end="")
        print("Life: ", game_state.life)
        print(" " * left_padding, end="")
        print("Score: ", game_state.score)
        self.get_print_game(game_state)
        print("\n" * ((size.lines - game_state.height) // 2), end="")
        print(" " * left_padding, end="")

    def get_print_game(self, game_state: GameState):
        size = os.get_terminal_size()
        left_padding = (size.columns - game_state.width) // 2
        if game_state.won:
            self.print_you_win(left_padding)
        elif game_state.life == 0:
            self.print_game_over(left_padding)
        else:
            self.print_board(game_state, left_padding)

    def print_board(self, game_state, left_padding):
        for row in game_state.maze:
            print(" " * left_padding, end="")
            print("".join(row))

    def print_game_over(self, left_padding):
        print(" " * left_padding, end="")
        print("Game Over")

    def print_you_win(self, left_padding):
        print(" " * left_padding, end="")
        print("You Win")


class TimerAdapter:

    def sleep(self, milliseconds: int) -> None:
        time.sleep(milliseconds/1000)


def main():
    pac_man = PacMan((1, 1))

    maze = Maze.from_str("""
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        w...ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff.....w
        w...wwwwwwwww..............................................wwwwwwwww...w
        w..f...wf......................................................w.......w
        w..f...wfwwwwwwwwwwwwwwwwwwwww..wwwwwwwwwwwwwwwwwwwwwwwwwwwww..w.......w
        w..f...wfw......ffffffffffffffffffffffffffffffffffff...........w.......w
        w..f...wfw..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww..w.......w
        w..f...wfw.....................................................w.......w
        w..f...wfw..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww..........w
        w..f...wfw.............................................................w
        w..f....f..............................................................w
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    """)

    ghosts = new_ghosts((4, 4))
    game = Game(maze, pac_man, ghosts)

    controller = Controller(game, TimerAdapter(), PresenterCli())

    ListenerInput(pac_man).start()

    for ghost in ghosts:
        RandomInput(ghost).start()

    controller.run()


if __name__ == '__main__':
    main()
