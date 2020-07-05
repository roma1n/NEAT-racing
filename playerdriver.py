import pygame as pg
from config import Controls


class PlayerDriver:
    def __init__(self):
        self.gas_pressed = False
        self.brake_pressed = False
        self.left_pressed = False
        self.right_pressed = False
    def drive(self, car, player_events):
        for event in player_events:
            if event.type == pg.KEYDOWN:
                if event.key == Controls.gas:
                    self.gas_pressed = True
                if event.key == Controls.brake:
                    self.brake_pressed = True
                if event.key == Controls.left:
                    self.left_pressed = True
                if event.key == Controls.right:
                    self.right_pressed = True

            if event.type == pg.KEYUP:
                if event.key == Controls.gas:
                    self.gas_pressed = False
                if event.key == Controls.brake:
                    self.brake_pressed = False
                if event.key == Controls.left:
                    self.left_pressed = False
                if event.key == Controls.right:
                    self.right_pressed = False

        gas = 0.5
        turn = 0.5

        if self.gas_pressed:
            gas += 0.5
        if self.brake_pressed:
            gas -= 0.5
        if self.left_pressed:
            turn += 0.5
        if self.right_pressed:
            turn -= 0.5

        car.drive(gas, turn)
