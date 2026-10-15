
import constants
from Character import Character
from Conveyor import Conveyor
from Package import Package
from Boss import Boss
from Truck import Truck
import pyxel


class Board:
    """
    Main game controller class. Coordinates all game objects and handles
    the game loop (update and draw). Delegates specific logic to the
    appropriate classes (Character, Conveyor, Truck, Boss).
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the game board and all game objects.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.__width = width
        self.__height = height
        self.__score = 0

        # Initialize characters
        self.__mario = Character("right", constants.MARIO_FIXED_X,
                                 constants.MARIO_START_Y, constants.MARIO_SPRITE)
        self.__luigi = Character("left", constants.LUIGI_FIXED_X,
                                 constants.LUIGI_START_Y, constants.LUIGI_SPRITE)

        # Initialize conveyors
        self.__conveyors = []
        for i in range(6):
            conveyor = Conveyor(i)
            self.__conveyors.append(conveyor)

        # Initialize truck and boss
        self.__truck = Truck(constants.TRUCK_SPRITE, constants.TRUCK_POSITION)
        self.__boss = Boss(constants.BOSS_SPRITE_LUIGI)

        # Game state variables
        self.__failures = 0
        self.__package_spawn_timer = constants.PACKAGE_SPAWN_INTERVAL
        self.__boss_was_active = False
        self.__truck_was_delivering = False

        # Start Pyxel
        pyxel.init(self.__width, self.__height, title="Pyxel game demo")
        pyxel.load("../resources.pyxres")
        pyxel.run(self.update, self.draw)

    # --- PROPERTIES ---

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    @property
    def mario(self):
        return self.__mario

    @property
    def luigi(self):
        return self.__luigi

    @property
    def conveyors(self):
        return self.__conveyors

    @property
    def truck(self):
        return self.__truck

    @property
    def boss(self):
        return self.__boss

    @property
    def failures(self):
        return self.__failures

    @failures.setter
    def failures(self, value):
        self.__failures = value

    # --- HELPER METHODS ---

    def get_total_packages(self):
        """Returns the total number of packages across all conveyors."""
        total = 0
        for conv in self.__conveyors:
            total += conv.get_package_count()
        return total

    def clear_all_packages(self):
        """Removes all packages from all conveyors."""
        for conveyor in self.__conveyors:
            conveyor.clear_packages()

    def get_catcher_for_conveyor(self, conveyor_idx: int):
        """Returns Mario for even conveyors, Luigi for odd."""
        if conveyor_idx % 2 == 0:
            return self.__mario
        else:
            return self.__luigi

    # --- GAME LOGIC METHODS ---

    def spawn_packages(self):
        """Spawns new packages on conveyor 0 if conditions are met."""
        if self.__package_spawn_timer > 0:
            self.__package_spawn_timer -= 1
        else:
            if self.get_total_packages() < 3:
                self.__conveyors[0].spawn_package()
            self.__package_spawn_timer = constants.PACKAGE_SPAWN_INTERVAL

    def move_packages(self):
        """Moves all packages on all conveyors."""
        move_freq = 30
        if pyxel.frame_count % move_freq == 0:
            for conveyor in self.__conveyors:
                conveyor.move_packages(constants.PACKAGE_STEP_SIZE)

    def check_transfers(self):
        """Checks if packages reached transfer points and handles them."""
        for conveyor in self.__conveyors:
            conveyor_idx = conveyor.level
            for package in list(conveyor.packages):
                self.process_package_transfer(package, conveyor_idx)

    def process_package_transfer(self, package, conveyor_idx: int):
        """Processes a package that may have reached a transfer point."""
        catcher = self.get_catcher_for_conveyor(conveyor_idx)
        transfer_x = catcher.get_transfer_x()
        blame_side = catcher.side
        direction = self.__conveyors[conveyor_idx].direction

        # Check if package reached transfer point
        if direction == -1:
            reached = package.x <= transfer_x
        else:
            reached = package.x >= transfer_x

        if reached:
            if catcher.can_catch_package(conveyor_idx):
                # SUCCESS
                self.__conveyors[conveyor_idx].remove_package(package)
                self.__score += 1

                next_conveyor = conveyor_idx + 1

                if next_conveyor >= 6:
                    self.__truck.load_package()
                    self.__score += 9
                else:
                    package.current_floor = next_conveyor
                    package.y = constants.CONVEYOR_Y_POSITIONS[next_conveyor]
                    package.x = catcher.get_next_package_x()
                    self.__conveyors[next_conveyor].add_package(package)
            else:
                # FAILURE
                self.__conveyors[conveyor_idx].remove_package(package)
                self.__failures += 1
                self.__boss.start_scolding(blame_side)

    def reset_game(self):
        """Resets the game to initial state."""
        self.__score = 0
        self.__failures = 0
        self.__boss.reset()
        self.__truck.reset()
        self.clear_all_packages()
        self.__mario.current_floor = 0
        self.__mario.y = constants.MARIO_START_Y
        self.__luigi.current_floor = 0
        self.__luigi.y = constants.LUIGI_START_Y
        self.__package_spawn_timer = constants.PACKAGE_SPAWN_INTERVAL

    # --- UPDATE METHOD ---

    def update(self):
        """Main update loop called every frame."""
        # Handle Game Over state
        if self.__boss.is_angry:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Check if boss just finished scolding
        if self.__boss_was_active and not self.__boss.is_active:
            self.clear_all_packages()
            self.__package_spawn_timer = constants.PACKAGE_SPAWN_INTERVAL
        self.__boss_was_active = self.__boss.is_active

        # Check if truck just started delivering
        if self.__truck.is_delivering and not self.__truck_was_delivering:
            self.clear_all_packages()
            self.__package_spawn_timer = constants.PACKAGE_SPAWN_INTERVAL
        self.__truck_was_delivering = self.__truck.is_delivering

        # Character input (delegated to each character)
        if not self.__boss.is_active:
            self.__mario.handle_input()
            self.__luigi.handle_input()

        # Package logic
        if not self.__boss.is_active and not self.__truck.is_delivering:
            self.spawn_packages()
            self.move_packages()
            self.check_transfers()

        # Update timers
        self.__truck.update()
        self.__boss.update()

    # --- DRAW METHOD ---

    def draw(self):
        """Main draw loop called every frame."""
        pyxel.cls(0)

        # Draw truck
        self.__truck.draw()

        # Draw conveyor belt sprites
        Conveyor.draw_all_conveyors()

        # Draw packages
        for conveyor in self.__conveyors:
            for package in conveyor.packages:
                package.draw()

        # Draw background
        self.draw_background()

        # Draw characters (unless being scolded)
        if not self.__boss.is_scolding_mario():
            pyxel.blt(self.__mario.fixed_x, self.__mario.y, 0, 16, 16, 16, 16, 0)
        if not self.__boss.is_scolding_luigi():
            pyxel.blt(self.__luigi.fixed_x, self.__luigi.y, 0, 0, 48, 16, 16, 0)

        # Draw boss scolding scene (delegated to Boss)
        self.__boss.draw_scolding_scene()

        # Draw HUD
        self.draw_hud()

        # Draw Game Over
        if self.__boss.is_angry:
            self.draw_game_over()

    def draw_background(self):
        """Draws background and static structures."""
        self.draw_central_column()
        self.draw_floor()
        self.draw_left_structure()
        self.draw_right_structure()

    def draw_central_column(self):
        """Draws the central dividing column."""
        for y_pos in range(0, constants.SCREEN_HEIGHT, 16):
            pyxel.blt(82, y_pos, 1, 32, 32, 16, 16, 0)

    def draw_floor(self):
        """Draws the floor tiles at the bottom."""
        for x_pos in range(0, constants.SCREEN_WIDTH, 16):
            pyxel.blt(x_pos, 164, 1, 16, 120, 16, 16, 0)

    def draw_left_structure(self):
        """Draws the left side structural elements."""
        pyxel.blt(19, 157, 1, 0, 136, 16, 16, 0)
        pyxel.blt(35, 156, 1, 16, 136, 16, 16, 0)
        pyxel.blt(21, 147, 1, 32, 136, 16, 16, 0)
        pyxel.blt(37, 147, 1, 32, 136, 16, 16, 0)
        pyxel.blt(0, 156, 1, 0, 120, 16, 16, 0)
        pyxel.blt(-11, 113, 1, 0, 104, 16, 16, 0)
        pyxel.blt(5, 113, 1, 0, 104, 16, 16, 0)
        pyxel.blt(21, 113, 1, 0, 104, 16, 16, 0)
        pyxel.blt(27, 109, 1, 32, 104, 16, 16, 0)
        pyxel.blt(27, 93, 1, 32, 104, 16, 16, 0)
        pyxel.blt(33, 77, 1, 0, 104, 16, 16, 0)
        pyxel.blt(35, 93, 1, 48, 104, 16, 16, 0)
        pyxel.blt(33, 111, 1, 0, 104, 16, 16, 0)
        pyxel.blt(35, 127, 1, 48, 104, 16, 16, 0)
        pyxel.blt(27, 113, 1, 16, 104, 16, 16, 0)
        pyxel.blt(27, 89, 1, 16, 152, -16, -16, 0)
        pyxel.blt(4, 67, 1, 16, 32, 16, 8, 0)

    def draw_right_structure(self):
        """Draws the right side structural elements."""
        pyxel.blt(125, 156, 1, 32, 136, 16, 16, 0)
        pyxel.blt(150, 156, 1, 48, 32, 16, 16, 0)
        pyxel.blt(166, 156, 1, 48, 88, 16, 16, 0)
        pyxel.blt(166, 140, 1, 48, 120, 16, 16, 0)
        pyxel.blt(166, 128, 1, 48, 136, 16, 16, 0)
        pyxel.blt(147, 149, 1, 0, 88, 16, 16, 0)
        pyxel.blt(125, 143, 1, 48, 104, 16, 16, 0)
        pyxel.blt(125, 129, 1, 32, 136, 16, 16, 0)
        pyxel.blt(141, 129, 1, 32, 136, 16, 16, 0)
        pyxel.blt(125, 114, 1, 48, 104, 16, 16, 0)
        pyxel.blt(125, 118, 1, 48, 104, 16, 16, 0)
        pyxel.blt(125, 98, 1, 32, 136, 16, 16, 0)

    def draw_hud(self):
        """Draws the HUD (floor indicators and score)."""
        # Mario floor indicator
        pyxel.blt(100, 1, 1, 32, 168, 32, 16, 0)
        pyxel.blt(129, 1, 1, 32, 184, 32, 16, 0)
        x_num, y_num = 151, 0
        if self.__mario.current_floor == 0:
            pyxel.blt(x_num, y_num, 1, 0, 168, 8, 16, 0)
        elif self.__mario.current_floor == 1:
            pyxel.blt(x_num, y_num, 1, 0, 184, 8, 16, 0)
        elif self.__mario.current_floor == 2:
            pyxel.blt(x_num, y_num, 1, 0, 200, 8, 16, 0)

        # Luigi floor indicator
        pyxel.blt(23, 1, 1, 32, 152, 32, 16, 0)
        pyxel.blt(47, 1, 1, 32, 184, 32, 16, 0)
        x_num, y_num = 69, 0
        if self.__luigi.current_floor == 0:
            pyxel.blt(x_num, y_num, 1, 0, 168, 8, 16, 0)
        elif self.__luigi.current_floor == 1:
            pyxel.blt(x_num, y_num, 1, 0, 184, 8, 16, 0)
        elif self.__luigi.current_floor == 2:
            pyxel.blt(x_num, y_num, 1, 0, 200, 8, 16, 0)

        # Score display
        pyxel.text(5, 20, "Score:" + str(self.__score), 7)
        pyxel.text(5, 30, "Fails:" + str(self.__failures), 8)

    def draw_game_over(self):
        """Draws the Game Over screen."""
        pyxel.rect(25, 60, 130, 50, 0)
        pyxel.rectb(25, 60, 130, 50, 8)
        pyxel.text(60, 75, "GAME OVER", 8)
        pyxel.text(40, 90, "Press R to restart", 7)
