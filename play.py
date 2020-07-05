from game import Game
from setuppygame import init_pygame, quit_pygame
from playerdriver import PlayerDriver


def play():
    window = init_pygame()
    game = Game(window, [PlayerDriver()])
    game.start()
    quit_pygame()


if __name__ == '__main__':
    play()