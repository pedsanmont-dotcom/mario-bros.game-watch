
import constants
import pyxel


class Boss:
    """
    Represents the game's authority figure (Boss), rendered only during a scolding
    event triggered by a package failure. The Boss remains hidden when not scolding.

    Temporary scolding lasts 3 seconds, becoming permanent (Game Over) after 3 failures.
    """

    # --- CLASS CONSTANTS ---

    BOSS_POSITIONS = {
        "Luigi": (50, 240),   # Position to scold Luigi (left side)
        "Mario": (200, 170)   # Position to scold Mario (right side)
    }

    def __init__(self, sprite=constants.BOSS_SPRITE_LUIGI):
        """
        Initializes the Boss logic. The Boss starts inactive.
        
        Args:
            sprite: Default boss sprite tuple
        """
        self.__failure_count = 0
        self.__is_angry = False
        self.__is_active = False
        self.__active_timer = 0
        self.__target_x = 0
        self.__target_y = 0
        self.__boss_sprite = sprite

    # --- PROPERTIES ---

    @property
    def failure_count(self):
        return self.__failure_count

    @property
    def is_angry(self):
        return self.__is_angry

    @property
    def is_active(self):
        return self.__is_active

    @property
    def target_x(self):
        return self.__target_x

    @property
    def target_y(self):
        return self.__target_y

    # --- METHODS ---

    def start_scolding(self, falling_side: str):
        """
        Triggers the boss scolding sequence.
        
        Args:
            falling_side: 'left' (culpable Luigi) or 'right' (culpable Mario)
        """
        falling_side = falling_side.lower().strip()

        # Activate scolding state
        self.__is_active = True
        self.__active_timer = constants.SCOLDING_DURATION

        # Determine who is being scolded based on the side
        character = "Luigi" if falling_side == "left" else "Mario"

        # Assign position
        if character in self.BOSS_POSITIONS:
            self.__target_x = self.BOSS_POSITIONS[character][0]
            self.__target_y = self.BOSS_POSITIONS[character][1]

        self.__failure_count += 1

        # Verify Game Over
        if self.__failure_count >= constants.MAX_FAILURES:
            self.__is_angry = True

    def is_scolding_mario(self):
        """
        Checks if the boss is currently scolding Mario.
        
        Returns:
            True if scolding Mario, False if scolding Luigi or not active
        """
        if not self.__is_active:
            return False
        return self.__target_x == self.BOSS_POSITIONS["Mario"][0]

    def is_scolding_luigi(self):
        """
        Checks if the boss is currently scolding Luigi.
        
        Returns:
            True if scolding Luigi, False if scolding Mario or not active
        """
        if not self.__is_active:
            return False
        return self.__target_x == self.BOSS_POSITIONS["Luigi"][0]

    def update(self):
        """Called every frame to update boss state."""
        if self.__is_active and not self.__is_angry:
            self.__active_timer -= 1
            if self.__active_timer <= 0:
                self.__is_active = False

    def draw(self):
        """Draw boss only when active."""
        if self.__is_active:
            pyxel.blt(self.__target_x, self.__target_y, *self.__boss_sprite)

    def draw_scolding_scene(self):
        """
        Draws the complete scolding scene (character being scolded + boss).
        Call this instead of draw() for the full scene.
        """
        if self.__is_active:
            if self.is_scolding_mario():
                # Draw Mario being scolded
                pyxel.blt(constants.MARIO_SCOLDED_X, constants.MARIO_SCOLDED_Y,
                          *constants.MARIO_SCOLDED_SPRITE)
                # Draw boss next to Mario
                pyxel.blt(constants.MARIO_SCOLDED_X + 15,
                          constants.MARIO_SCOLDED_Y + 4,
                          *constants.BOSS_SPRITE_MARIO)
            else:
                # Draw Luigi being scolded
                pyxel.blt(constants.LUIGI_SCOLDED_X, constants.LUIGI_SCOLDED_Y,
                          *constants.LUIGI_SCOLDED_SPRITE)
                # Draw boss next to Luigi
                pyxel.blt(constants.LUIGI_SCOLDED_X - 16,
                          constants.LUIGI_SCOLDED_Y + 12,
                          *constants.BOSS_SPRITE_LUIGI)

    def reset(self):
        """Reset boss state for new game."""
        self.__failure_count = 0
        self.__is_angry = False
        self.__is_active = False
        self.__active_timer = 0
