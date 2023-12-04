

from typing import Protocol
from pacman.game import Game, GameState


class Timer(Protocol):
    def sleep(self, milliseconds: int) -> None:
        ...


class Presenter(Protocol):
    def present(self, game_state: GameState) -> None:
        ...


class Controller:

    def __init__(self, game: Game, timer: Timer, presenter: Presenter):
        self.timer = timer
        self.game = game
        self.presenter = presenter

    def run(self) -> None:
        while not self.game.won:
            self.timer.sleep(100)
            self.game.next_frame()
            self.presenter.present(
                self.game.to_game_state())
