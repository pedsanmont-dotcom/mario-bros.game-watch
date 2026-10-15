
import pyxel
import constants


class Package:
    """
    Represents a package moving through the conveyor system using absolute 
    screen coordinates (x, y) and discrete steps (jumps).
    """

    def __init__(self, x_start: int, y_start: int, current_floor: int):
        """
        Create a new package at absolute screen coordinates.

        Args:
            x_start (int): Starting X coordinate on the screen.
            y_start (int): Starting Y coordinate on the screen.
            current_floor (int): Starting conveyor level (usually 0).
        """
        self.__current_floor = current_floor
        self.__x = x_start
        self.__y = y_start

    # --- PROPERTIES AND SETTERS ---

    @property
    def current_floor(self):
        return self.__current_floor

    @current_floor.setter
    def current_floor(self, value):
        if not isinstance(value, int):
            raise TypeError("Conveyor level must be an integer")
        if value < 0:
            raise ValueError("Conveyor level must be non-negative")
        self.__current_floor = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = int(value)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = int(value)

    # --- SPRITE METHOD ---

    def get_sprite(self):
        """
        Get the appropriate sprite based on the package's current level.
        """
        if self.__current_floor <= 1:
            return constants.PACKAGE_1st_SPRITE
        elif self.__current_floor == 2:
            return constants.PACKAGE_2nd_SPRITE
        elif self.__current_floor == 3:
            return constants.PACKAGE_3rd_SPRITE
        elif self.__current_floor == 4:
            return constants.PACKAGE_4th_SPRITE
        else:
            return constants.PACKAGE_5th_SPRITE

    # --- DRAW METHOD ---

    def draw(self):
        """Draw the package at its absolute screen coordinates."""
        pyxel.blt(self.__x, self.__y, *self.get_sprite())
