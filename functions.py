from random import randint, uniform
from Map import CellType
from Agent import Agent


def random_walk_2d(map_obj, start, tiles):
    """ Generates a map based on random walk """
    width = map_obj.get_width()
    height = map_obj.get_height()

    p = start
    not_in_boundary = 1
    map_obj.set_xy(p[0], p[1])
    number_tiles = width * height * tiles
    count = 0
    while count < number_tiles:
        while not_in_boundary:
            rnd = randint(0, 3)
            if rnd == 0 and p[0] > 0:             # move left
                p = p[0] - 1, p[1]
                not_in_boundary = 0
            elif rnd == 1 and p[0] < width - 1:   # move right
                p = p[0] + 1, p[1]
                not_in_boundary = 0
            elif rnd == 2 and p[1] > 0:           # move down
                p = p[0], p[1] - 1
                not_in_boundary = 0
            elif rnd == 3 and p[1] < height - 1:  # move up
                p = p[0], p[1] + 1
                not_in_boundary = 0
        not_in_boundary = 1
        if map_obj.get_xy_value(p[0], p[1]) == CellType.WALL:
            count += 1
        map_obj.set_xy(p[0], p[1])
