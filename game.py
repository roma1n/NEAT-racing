import pygame as pg
from config import GameConfig, Level
import math


class Road:
    def __init__(self, sprite_path, x, y):
        self.sprite = pg.image.load(sprite_path)
        self.x = x
        self.y = y

    def draw(self, window):
        rect = self.sprite.get_rect(center=(self.x, self.y))
        window.blit(self.sprite, rect.topleft)


class Car:
    def __init__(self, sprite_path, x, y, rotation):
        self.sprite = pg.transform.flip(pg.image.load(sprite_path), False, True)
        self.x = x
        self.y = y
        self.rotation = rotation
        self.radar_angles = GameConfig.car_radar_angles
        self.radar_max_lengths = GameConfig.car_radar_max_lengths
        self.radar_lengths = [0, 0, 0, 0, 0]
        self.alive = True

    def rotared_sprite(self):
        return pg.transform.rotate(self.sprite, -self.rotation)

    def update_radars(self, window):
        # upadte aliveness
        for point in GameConfig.car_anchor_points:
            point = pg.Vector2(*point).rotate(self.rotation)
            point = (int(self.x + point.x), int(self.y + point.y))
            if point[0] < 0 or point[0] >= 1920 or point[1] < 0 or point[1] >= 1080 or \
                window.get_at(point) == (0, 150, 0, 255):
                self.alive = False

        self.radar_lengths = [0, 0, 0, 0, 0]

        if not self.alive:
            return

        for num, t in enumerate(zip(
            self.radar_angles, 
            self.radar_max_lengths, 
            self.radar_lengths
        )):
            angle, max_lenght, length = t
            angle += self.rotation
            c = math.cos(math.radians(angle))
            s = math.sin(math.radians(angle))

            while int(self.x + length * c) >= 0 and int(self.x + length * c) < 1920 and \
                    int(self.y + length * s) >= 0 and int(self.y + length * s) < 1080 and \
                    window.get_at((int(self.x + length * c), int(self.y + length * s))) != (0, 150, 0, 255) and length < max_lenght:
                length += 1

            if length == 0:
                self.alive = False
            self.radar_lengths[num] = length

    def draw_radars(self, window):
        for angle, length in zip(self.radar_angles, self.radar_lengths):
            angle += self.rotation
            c = math.cos(math.radians(angle))
            s = math.sin(math.radians(angle))
            end_pos = (self.x + int(length * c), self.y + int(length * s))
            pg.draw.line(window, (255, 0, 0), (self.x, self.y), end_pos, 3)

    def drive(self, gas, turn):
        '''
        :param gas:  gas for car, valid values: [0, 1]
        :param turn: rotation of steering wheel, valid values: [0, 1]
        '''
        if not self.alive:
            return
        
        self.rotation -= GameConfig.min_angular_velocity * (1 - turn) + GameConfig.max_angular_velocity * turn

        c = math.cos(math.radians(90 + self.rotation))
        s = math.sin(math.radians(90 + self.rotation))

        self.x += c * (GameConfig.min_velocity * (1 - gas) + GameConfig.max_velocity * gas)
        self.y += s * (GameConfig.min_velocity * (1 - gas) + GameConfig.max_velocity * gas)
        

    def draw(self, window):
        if not self.alive:
            return

        current_sprite = self.rotared_sprite()
        rect = current_sprite.get_rect(center=(self.x, self.y))

        self.update_radars(window)

        if GameConfig.car_draw_radars:
            self.draw_radars(window)

        window.blit(current_sprite, rect.topleft)


class Game:
    def __init__(self, window, drivers, info=None):
        self.font = pg.font.Font('fonts/SourceSansPro-Black.otf', 40)
        self.window = window
        self.drivers = drivers
        self.info=info
        self.cars = []
        for i in range(len(drivers)):
            self.cars.append(Car(GameConfig.car_sprite_path, 1000, 988, 270))
        self.cars_alive = len(self.cars)
        self.roads = []

        for y in range(len(Level.structure)):
            for x in range(len(Level.structure[y])):
                pos = (320 + 128 * x, 92 + 128 * y)
                if Level.structure[y][x] == 'g':
                    pass
                elif Level.structure[y][x] == 'v':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[0], *pos)
                    )
                elif Level.structure[y][x] == 's':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[1], *pos)
                    )
                elif Level.structure[y][x] == 'lu':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[40], *pos)
                    )
                elif Level.structure[y][x] == 'dr':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[2], *pos)
                    )
                elif Level.structure[y][x] == 'ru':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[38], *pos)
                    )
                elif Level.structure[y][x] == 'ld':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[4], *pos)
                    )
                elif Level.structure[y][x] == 'f':
                    self.roads.append(
                        Road(GameConfig.road_sprite_paths[42], *pos)
                    )

    def on_exit(self, status):
        if status == 'quit':
            exit()

    def draw(self):
        pg.draw.rect(self.window, (0, 150, 0), (0, 0, 1920, 1080))
        for road in self.roads:
            road.draw(self.window)

        for car in self.cars:
            car.draw(self.window)

        if self.info is not None:
                for num, line in enumerate(self.info().split('\n')):
                    text = self.font.render(line, True, (100, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.topleft = (1300, 40 + num * 40)
                    self.window.blit(text, text_rect)

        pg.display.update()

    def start(self, max_time = -1):
        time = 0
        clock = pg.time.Clock()
        running = True
        while running:
            self. draw()

            player_events = []

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return self.on_exit('quit')
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return self.on_exit('quit')
                else:
                    player_events.append(event)

            for dirver, car in zip(self.drivers, self.cars):
                dirver.drive(car, player_events)

            self.cars_alive = 0
            for car in self.cars:
                if car.alive:
                    self.cars_alive += 1

            if self.cars_alive == 0:
                running = False

            time += 1
            if time == max_time:
                running = False

            clock.tick(60)
