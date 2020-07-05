import pygame as pg


class Level:
    '''
    v -- vertical
    s -- stright (hotizontal)
    lu -- left to up
    dr -- down to right
    ru -- right to up
    ld -- down to left
    g -- grass
    f -- finish
    '''
    structure = [
        ['dr', 's', 's', 's', 's', 's', 'ld', 'g', 'g', 'g', 'g'],
        ['v', 'g', 'g', 'g', 'g', 'g', 'v', 'g', 'g', 'g', 'g'],
        ['v', 'g', 'g', 'g', 'g', 'g', 'ru', 's', 's', 's', 'ld'],
        ['v', 'g', 'dr', 's', 'ld', 'g', 'g', 'g', 'g', 'g', 'v'],
        ['v', 'g', 'v', 'g', 'v', 'g', 'g', 'g', 'g', 'g', 'v'],
        ['v', 'g', 'v', 'g', 'v', 'g', 'g', 'g', 'dr', 's', 'lu'],
        ['v', 'g', 'v', 'g', 'v', 'g', 'g', 'g', 'v', 'g', 'g'],
        ['ru', 's', 'lu', 'g', 'ru', 's', 'f', 's', 'lu', 'g', 'g'],
    ]


class GameConfig:
    # car
    min_velocity = 5
    max_velocity = 10
    min_angular_velocity = -5
    max_angular_velocity = 5
    car_radar_angles = [90, 0, 180, 45, 135]
    car_radar_max_lengths = [250, 100, 100, 200, 200]
    car_anchor_points = [(15, 30), (-15, 30), (15, -30), (-15, -30), (0, 30), (0, -30)]
    car_draw_radars = True

    # sprite paths
    car_sprite_path = 'pics/cars/car_blue_small_1.png'
    
    def get_road_sprites_paths():
        res = []
        for i in range(1, 90):
            s = str(i)
            if len(s) < 2:
                s = '0' + s

            res.append('pics/tiles/asphalt road/road_asphalt{}.png'.format(s))

        return res

    road_sprite_paths = get_road_sprites_paths()


class Controls:
    gas = pg.K_w
    brake = pg.K_s
    left = pg.K_a
    right = pg.K_d