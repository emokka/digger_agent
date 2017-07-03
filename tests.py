import unittest
from random import randint
from Map import Map, Cell, CellType
from Agent import Agent
from functions import random_walk_2d


class TestOutput(unittest.TestCase):

    def test_map_array(self):
        width = 50
        height = 50
        cell_size = 10
        arr = []
        for i in range(0, height):
            for j in range(0, width):
                if i == j:
                    c = Cell(i, j, CellType.CORRIDOR)
                    arr.append(c)
                else:
                    c = Cell(i, j, CellType.WALL)
                    arr.append(c)
        m = Map(width, height, cell_size)
        m.set_array(arr)
        img_width, img_height = m.get_img_size()
        self.assertEqual(img_width, width * cell_size)
        self.assertEqual(img_height, height * cell_size)
        for i in range(0, height):
            for j in range(0, width):
                if i == j:
                    self.assertEqual(m.get_xy_value(i, j), CellType.CORRIDOR)
                else:
                    self.assertEqual(m.get_xy_value(i, j), CellType.WALL)

    def test_random_walk(self):
        width = 100
        height = 100
        cell_size = 10
        arr = []
        for i in range(0, height):
            for j in range(0, width):
                c = Cell(i, j, CellType.WALL)
                arr.append(c)
        m = Map(width, height, cell_size)
        m.set_array(arr)
        start = randint(0, width), randint(0, height)
        tile_per = 0.4
        random_walk_2d(m, start, tile_per)
        # m.print()

    def test_dig_random(self):
        width = 100
        height = 100
        cell_size = 10
        arr = []
        for i in range(0, height):
            for j in range(0, width):
                c = Cell(i, j, CellType.WALL)
                arr.append(c)
        m = Map(width, height, cell_size)
        m.set_array(arr)
        start = m.get_xy(randint(0, width), randint(0, height))
        tiles = 0.4
        a = Agent()
        a.dig(m, start, tiles, 0)
        # m.print()

    def test_dig_maze(self):
        width = 50
        height = 50
        cell_size = 10
        arr = []
        for i in range(0, height):
            for j in range(0, width):
                c = Cell(i, j, CellType.WALL)
                arr.append(c)
        m = Map(width, height, cell_size)
        m.set_array(arr)
        start = m.get_xy(randint(0, width), randint(0, height))
        tiles = 0.3
        a = Agent()
        a.dig(m, start, tiles, 1)
        # m.print()

    def test_dig_maze_rand(self):
        width = 100
        height = 100
        cell_size = 10
        arr = []
        for i in range(0, height):
            for j in range(0, width):
                c = Cell(i, j, CellType.WALL)
                arr.append(c)
        m = Map(width, height, cell_size)
        m.set_array(arr)
        start = m.get_xy(randint(0, width), randint(0, height))
        tiles = 0.3
        a = Agent()
        a.dig(m, start, tiles, 2)
        # m.print()

    def test_dig_new_maze(self):
        width = 50
        height = 50
        cell_size = 50
        arr = []
        for i in range(0, height):
            for j in range(0, width):
                c = Cell(i, j, CellType.WALL)
                arr.append(c)
        m = Map(width, height, cell_size)
        m.set_array(arr)
        start = m.get_xy(randint(0, width), randint(0, height))
        tiles = 0.4
        a = Agent()
        a.dig(m, start, tiles, 3)
        m.print()

if __name__ == '__main__':
    unittest.main()

TestOutput.main()
