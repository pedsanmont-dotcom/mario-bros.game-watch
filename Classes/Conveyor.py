
import constants
import pyxel
from Package import Package


class Conveyor:
    """
    Represents a single conveyor belt. Acts as a container for packages
    at a specific level (floor). Handles package movement and spawning.
    """

    def __init__(self, level: int):
        """
        Initializes one conveyor belt.

        Args:
            level (int): Conveyor level index (0=bottom, 1, 2, ... N=top)
        """
        self.__level = level
        self.__y = constants.CONVEYOR_Y_POSITIONS[level]

        # Movement direction: conveyors 2 and 4 move RIGHT, all others move LEFT
        if level == 2 or level == 4:
            self.__direction = 1  # RIGHT
        else:
            self.__direction = -1  # LEFT

        self.__packages = []

    # --- PROPERTIES ---

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        if value not in [-1, 1]:
            raise ValueError("Direction must be -1 or +1")
        self.__direction = value

    @property
    def y(self):
        return self.__y

    @property
    def packages(self):
        return self.__packages

    @packages.setter
    def packages(self, value):
        self.__packages = value

    # --- PACKAGE MANAGEMENT METHODS ---

    def add_package(self, package):
        """Adds a package to this conveyor."""
        self.__packages.append(package)

    def remove_package(self, package):
        """Removes a package from this conveyor."""
        if package in self.__packages:
            self.__packages.remove(package)

    def clear_packages(self):
        """Removes all packages from this conveyor."""
        self.__packages = []

    def get_package_count(self):
        """Returns the number of packages on this conveyor."""
        return len(self.__packages)

    def move_packages(self, step: int):
        """
        Moves all packages on this conveyor by the given step.
        
        Args:
            step: Number of pixels to move (from constants.PACKAGE_STEP_SIZE)
        """
        for package in list(self.__packages):
            package.x += self.__direction * step

    def spawn_package(self):
        """
        Creates a new package on this conveyor.
        Only conveyor 0 should call this method.
        
        Returns:
            The newly created package
        """
        start_x = constants.PKG_START_X["right"]
        start_y = constants.CONVEYOR_Y_POSITIONS[self.__level]
        new_package = Package(start_x, start_y, self.__level)
        self.__packages.append(new_package)
        return new_package

    # --- DRAW METHODS ---

    @staticmethod
    def draw_all_conveyors():
        """Draws all conveyor belt sprites on the screen."""
        pyxel.blt(96, 149, 1, 0, 88, 16, 16, 0)
        pyxel.blt(104, 149, 1, 0, 88, 16, 16, 0)
        pyxel.blt(96, 132, 1, 0, 88, 16, 16, 0)
        pyxel.blt(104, 132, 1, 0, 88, 16, 16, 0)
        pyxel.blt(96, 115, 1, 0, 88, 16, 16, 0)
        pyxel.blt(104, 115, 1, 0, 88, 16, 16, 0)
        pyxel.blt(96, 98, 1, 0, 88, 16, 16, 0)
        pyxel.blt(104, 98, 1, 0, 88, 16, 16, 0)
        pyxel.blt(60, 149, 1, 0, 88, 16, 16, 0)
        pyxel.blt(68, 149, 1, 0, 88, 16, 16, 0)
        pyxel.blt(60, 132, 1, 0, 88, 16, 16, 0)
        pyxel.blt(68, 132, 1, 0, 88, 16, 16, 0)
        pyxel.blt(60, 115, 1, 0, 88, 16, 16, 0)
        pyxel.blt(68, 115, 1, 0, 88, 16, 16, 0)
        pyxel.blt(60, 98, 1, 0, 88, 16, 16, 0)
        pyxel.blt(68, 98, 1, 0, 88, 16, 16, 0)
        pyxel.blt(60, 81, 1, 0, 88, 16, 16, 0)
        pyxel.blt(68, 81, 1, 0, 88, 16, 16, 0)
        pyxel.blt(96, 81, 1, 0, 88, 16, 16, 0)
        pyxel.blt(104, 81, 1, 0, 88, 16, 16, 0)
