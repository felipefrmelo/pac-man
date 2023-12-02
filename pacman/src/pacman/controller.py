

from dataclasses import dataclass
from typing import Protocol
from pacman.game import Game


class Timer(Protocol):
    def sleep(self, milliseconds: int) -> None:
        ...


@dataclass
class GameState:
    score: int
    won: bool
    life: int
    maze: list[list[str]]

    @property
    def height(self) -> int:
        return len(self.maze)

    @property
    def width(self) -> int:
        return len(self.maze[0])


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
            self.presenter.present(GameState(
                score=self.game.score,
                life=self.game.life,
                won=self.game.won,
                maze=self.game.to_list()
            ))
