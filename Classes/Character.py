
import pyxel
import constants


class Character:
    """
    Manages a static character (Mario/Luigi) fixed in X, able to move vertically (Y)
    and handle package transfers between conveyors.
    """

    def __init__(self, side: str, fixed_x: int, y: int, sprite: tuple):
        """
        Initialize the character.
        
        Args:
            side: 'left' or 'right' (for Luigi/Mario)
            fixed_x: constant X position from constants
            y: initial Y position
            sprite: pyxel sprite tuple (bank, x, y, width, height)
        """
        self.__side = side.lower().strip()
        if self.__side not in ["right", "left"]:
            raise ValueError("Side must be either 'right' or 'left'")
            
        self.__fixed_x = fixed_x
        self.__y = y
        self.__sprite = sprite
        self.__current_floor = 0
        
        # Set control keys based on side
        if self.__side == "right":
            # Mario uses arrow keys
            self.__key_up = pyxel.KEY_UP
            self.__key_down = pyxel.KEY_DOWN
            self.__floor_positions = constants.MARIO_FLOOR_POSITIONS
        else:
            # Luigi uses W/S keys
            self.__key_up = pyxel.KEY_W
            self.__key_down = pyxel.KEY_S
            self.__floor_positions = constants.LUIGI_FLOOR_POSITIONS

    # --- PROPERTIES ---

    @property
    def side(self):
        return self.__side

    @property
    def fixed_x(self):
        return self.__fixed_x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Y must be int or float")
        self.__y = value

    @property
    def sprite(self):
        return self.__sprite

    @property
    def current_floor(self):
        return self.__current_floor

    @current_floor.setter
    def current_floor(self, value):
        self.__current_floor = value

    # --- INPUT HANDLING ---

    def handle_input(self):
        """
        Handles keyboard input for this character's movement.
        Each character has its own keys configured in __init__.
        """
        if pyxel.btnp(self.__key_up):
            self.change_floor("up")
        if pyxel.btnp(self.__key_down):
            self.change_floor("down")

    # --- MOVEMENT METHODS ---

    def change_floor(self, direction: str):
        """
        Moves the character between floors based on the direction.
        
        Args:
            direction: "up" or "down"
        """
        direction = direction.lower().strip()

        if direction == "up":
            if self.__current_floor < len(self.__floor_positions) - 1:
                self.__current_floor += 1
                self.__y = self.__floor_positions[self.__current_floor]

        elif direction == "down":
            if self.__current_floor > 0:
                self.__current_floor -= 1
                self.__y = self.__floor_positions[self.__current_floor]

    # --- PACKAGE HANDLING METHODS ---

    def get_transfer_x(self):
        """Returns the X position where this character catches packages."""
        if self.__side == "right":
            return self.__fixed_x
        else:
            return self.__fixed_x + 5

    def get_required_floor_for_conveyor(self, conveyor_idx: int):
        """
        Returns the floor this character needs to be on to catch 
        packages from the given conveyor.
        
        Args:
            conveyor_idx: The conveyor level index
            
        Returns:
            The floor number required
        """
        if self.__side == "right":
            # Mario: conv 0->floor 0, conv 2->floor 1, conv 4->floor 2
            return conveyor_idx // 2
        else:
            # Luigi: conv 1->floor 0, conv 3->floor 1, conv 5->floor 2
            return (conveyor_idx - 1) // 2

    def can_catch_package(self, conveyor_idx: int):
        """
        Checks if this character can catch a package from the given conveyor.
        
        Args:
            conveyor_idx: The conveyor level index
            
        Returns:
            True if character is on the correct floor
        """
        required_floor = self.get_required_floor_for_conveyor(conveyor_idx)
        return self.__current_floor == required_floor

    def get_next_package_x(self):
        """
        Returns the X position where this character places packages 
        on the next conveyor.
        """
        if self.__side == "right":
            # Mario places packages to his left
            return self.__fixed_x - 17
        else:
            # Luigi places packages to his right
            return self.__fixed_x + 23

    # --- DRAW METHOD ---

    def draw(self):
        """Draws the character at its current position."""
        pyxel.blt(self.__fixed_x, self.__y, *self.__sprite)
