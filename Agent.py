import math
from random import randint, uniform
from Map import Cell, CellType


class Agent:
    """ Autonomous agent that walks over a map doing things """

    __cell = Cell()
    __current_direction = 0
    __current_state = 0

    RULES = ['drunkard', 'maze', 'maze_rand', 'new_maze']
    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, cell=Cell(), a=(0, 0)):
        self.__cell = cell

    def move_and_set(self, target, value=CellType.WALL):
        target.set_type(value)
        self.__cell = target

    def get_position(self):
        """ gets current position """
        return self.__cell.get_xy()

    def dig(self, map_obj, start, tile_per, rule):
        """ Crawls all over the map and acts according to a rule """
        p = start
        number_tiles = map_obj.get_width() * map_obj.get_height() * tile_per
        self.move_and_set(p, CellType.CORRIDOR)
        count = 1
        while count < number_tiles:
            p = getattr(self, self.RULES[rule])(map_obj, p)
            if p.get_type() == CellType.WALL:
                count += 1
            self.move_and_set(p, CellType.CORRIDOR)

    def drunkard(self, map_obj, p):
        """ cave like map """
        in_boundary = 0
        while not in_boundary:
            rnd = randint(0, 3)
            direction = self.DIRECTIONS[rnd]
            pos = p.get_xy()
            new_pos = pos[0] + direction[0], pos[1] + direction[1]
            if map_obj.is_in_boundary(new_pos):
                in_boundary = 1
                self.__current_direction = rnd
        return map_obj.get_xy(new_pos[0], new_pos[1])

    def maze(self, map_obj, p):
        """ kind of a maze """
        in_boundary = 0
        next_cell = Cell()
        while not in_boundary:
            rnd = uniform(0, 1)
            if rnd < 0.95:
                # High chance of corridors
                direction = self.DIRECTIONS[self.__current_direction]
                pos = p.get_xy()
                new_pos = pos[0] + direction[0], pos[1] + direction[1]
                if map_obj.is_in_boundary(new_pos):
                    in_boundary = 1
                    next_cell = map_obj.get_xy(new_pos[0], new_pos[1])
            else:
                next_cell = self.drunkard(map_obj, p)
        return next_cell

    def maze_rand(self, map_obj, p):
        """ Mix between maze and random """
        # self.__current_state = randint(0, 1)
        rnd = uniform(0, 1)
        if rnd > 0.6:
            # chance to switch to another state
            self.__current_state = randint(0, 1)
        return getattr(self, self.RULES[self.__current_state])(map_obj, p)

    def new_maze(self, map_obj, p):
        """ kind of a maze """
        in_boundary = 0
        next_cell = p
        while not in_boundary:
            direction = self.DIRECTIONS[randint(0, 3)]
            pos = p.get_xy()
            new_pos = pos[0] + direction[0], pos[1] + direction[1]
            if map_obj.is_in_boundary(new_pos):
                if not self.check_cycle(map_obj, new_pos[0], new_pos[1]):
                    in_boundary = 1
                    next_cell = map_obj.get_xy(new_pos[0], new_pos[1])
        return next_cell

    def check_cycle(self, map_obj, x, y):
        """ we consider p and its neighbour as a graph and we check fo cycles """
        cycle = 0
        environment = self.get_environment(map_obj, x, y)
        white_nodes = [node for node, env in environment.items()]
        gray_nodes = []
        black_nodes = []
        stack = []
        stack.append(4)
        white_nodes.remove(4)
        gray_nodes.append(4)
        while stack:
            node = stack.pop()
            neighbours = environment[node]
            for n in neighbours:
                if n in gray_nodes:
                    cycle = 1
                    return cycle
                elif n in white_nodes:
                    stack.append(n)
                    white_nodes.remove(n)
                    gray_nodes.append(n)
            gray_nodes.remove(node)
            black_nodes.append(node)
        return cycle

    def get_environment(self, map_obj, x, y):
        directions = {
            0: (-1, 1),
            1: (0, 1),
            2: (1, 1),
            3: (-1, 0),
            # 4: (0, 0),  # we assume (x,y) will be corridor and in boundary
            5: (1, 0),
            6: (-1, -1),
            7: (0, -1),
            8: (1, -1)
        }
        environment = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4, 6],
            4: [1, 3, 5, 7],
            5: [2, 4, 8],
            6: [3, 7],
            7: [4, 6, 8],
            8: [5, 7]
        }
        remove =[]
        for node, direction in directions.items():
            xx, yy = x + directions[node][0], y + directions[node][1]
            if not map_obj.is_in_boundary((xx, yy)):
                remove.append(node)
            else:
                cell = map_obj.get_xy(xx, yy)
                if cell.get_type() == CellType.WALL:
                    remove.append(node)

        for r in remove:
            del directions[r]
            del environment[r]

        for n, neighbours in environment.items():
            for r in remove:
                if r in neighbours:
                    neighbours.remove(r)

        return environment
