from enum import Enum
from PIL import Image


class CellType(Enum):
    ROOM = 1,
    WALL = 0,
    CORRIDOR = 1


class Cell:
    """ A cell in the map """

    __type = CellType.WALL
    __x = 0
    __y = 0

    def __init__(self, x=0, y=0, typ=CellType.WALL):
        self.__x = x
        self.__y = y
        self.__type = typ

    def get_type(self):
        return self.__type

    def get_xy(self):
        return self.__x, self.__y

    def set_type(self, t):
        self.__type = t


class Map:
    """ Stores the map """

    __map_array = []    # list of Cell objects
    __total_width = 0   # px
    __total_height = 0  # px
    __width = 0         # cells
    __height = 0        # cells
    __cell_size = 1     # px

    def __init__(self, width, height, cell_size):
        self.__width = width
        self.__height = height
        self.__cell_size = cell_size
        self.__total_width = width * self.__cell_size
        self.__total_height = height * self.__cell_size

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_xy_value(self, x, y):
        index = self.__width * x + y
        c = self.__map_array[index]
        return c.get_type()

    def get_xy(self, x, y):
        index = self.__width * x + y
        return self.__map_array[index]

    def get_img_size(self):
        return self.__total_width, self.__total_height

    def set_array(self, arr):
        self.__map_array = arr

    def set_xy(self, x, y, value=CellType.CORRIDOR):
        index = self.__width * x + y
        c = Cell(x, y, value)
        self.__map_array[index] = c

    def is_in_boundary(self, position):
        in_boundary = 0
        if position[0] in range(0, self.__width) and position[1] in range(0, self.__height):
            in_boundary = 1
        return in_boundary

    def print(self):

        print_arr = []

        for i in range(0, self.__total_height):
            for j in range(0, self.__total_width):
                x = i // self.__cell_size
                y = j // self.__cell_size
                print_arr.append(self.get_xy_value(x, y).value)

        im = Image.new("1", (self.__total_width, self.__total_height), "white")
        im.putdata(print_arr)
        im.show()
