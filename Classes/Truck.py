
import constants
import pyxel


class Truck:
    """
    Represents the delivery truck that receives packages from Luigi.
    When it has 8 packages, it goes out for delivery.
    """
    
    # Sprites for truck back with packages (img 1)
    TRUCK_BACK_SPRITES = [
        (1, 0, 152, 16, 16),     # 0 packages
        (1, 0, 48, 16, 16),      # 1 package
        (1, 16, 48, 16, 16),     # 2 packages
        (1, 32, 48, 16, 16),     # 3 packages
        (1, 48, 48, 16, 16),     # 4 packages
        (1, 64, 48, 16, 16),     # 5 packages
        (1, 80, 48, 16, 16),     # 6 packages
        (1, 96, 48, 16, 16),     # 7 packages
        (1, 112, 48, 16, 16),    # 8 packages
    ]

    def __init__(self, sprite: tuple, position: tuple):
        """
        Initializes the truck.
        
        Args:
            sprite: Front sprite tuple (driver part)
            position: (x, y) position tuple
        """
        self.__front_sprite = sprite
        self.__x = position[0]
        self.__y = position[1]
        self.__package_count = 0
        self.__is_delivering = False
        self.__max_packages = 8
        self.__delivery_duration = 180  # 3 seconds at 60 FPS
        self.__delivery_timer = 0

    # --- PROPERTIES ---

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def package_count(self):
        return self.__package_count

    @property
    def is_delivering(self):
        return self.__is_delivering

    @property
    def max_packages(self):
        return self.__max_packages

    # --- METHODS ---

    def load_package(self):
        """Adds a package to the truck. Starts delivery when full."""
        if not self.__is_delivering:
            self.__package_count += 1
            if self.__package_count >= self.__max_packages:
                self.start_delivery()

    def start_delivery(self):
        """Truck goes out for delivery."""
        self.__is_delivering = True
        self.__delivery_timer = self.__delivery_duration

    def finish_delivery(self):
        """Truck returns from delivery."""
        self.__is_delivering = False
        self.__package_count = 0

    def update(self):
        """Updates the delivery timer every frame."""
        if self.__is_delivering:
            self.__delivery_timer -= 1
            if self.__delivery_timer <= 0:
                self.finish_delivery()

    def draw(self):
        """Draws the truck (only when not delivering)."""
        if not self.__is_delivering:
            # Draw truck front (driver part)
            pyxel.blt(self.__x, self.__y, *self.__front_sprite)
            
            # Draw truck back (always drawn, sprite changes based on package count)
            back_sprite = self.TRUCK_BACK_SPRITES[self.__package_count]
            pyxel.blt(self.__x + 16, self.__y, *back_sprite)

    def reset(self):
        """Resets truck to initial state."""
        self.__package_count = 0
        self.__is_delivering = False
        self.__delivery_timer = 0
