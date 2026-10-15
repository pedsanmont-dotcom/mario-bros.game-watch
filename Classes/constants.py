"""
Class that groups the constants to be used in the game.
"""

#------------------------------------
# ============== SCREEN ==============
#------------------------------------
SCREEN_WIDTH = 180
SCREEN_HEIGHT = 180

#------------------------------------
# ============== MARIO ==============
#------------------------------------
MARIO_FIXED_X = 127
MARIO_START_Y = 153  # Floor 0 (down)
MARIO_SPRITE = (0, 16, 16, 16, 16)  # Normal Mario's sprite

MARIO_FLOOR_POSITIONS = [153, 126, 95]

# Mario's sprite being scolded (different position)
MARIO_SCOLDED_X = 145
MARIO_SCOLDED_Y = 126
MARIO_SCOLDED_SPRITE = (0, 0, 16, 16, 16)

#------------------------------------
# ============== LUIGI ==============
#------------------------------------

LUIGI_FIXED_X = 36
LUIGI_START_Y = 144  # Floor 0 (down)
LUIGI_SPRITE = (0, 0, 48, 16, 16)  # Normal Luigi's sprite

LUIGI_FLOOR_POSITIONS = [144, 107, 73]

LUIGI_SCOLDED_X = 17
LUIGI_SCOLDED_Y = 144
LUIGI_SCOLDED_SPRITE = (0, 0, 32, 16, 16)

#------------------------------------
# ======= FLOORS / CONVEYORS =======
#------------------------------------

# Y positions of each conveyor belt
CONVEYOR_Y_POSITIONS = [154, 154, 134, 116, 100, 78]

PKG_START_X = {
    "right": 147,
    "left": 60
}

#------------------------------------
# ============== TRUCK ==============
#------------------------------------

TRUCK_SPRITE = (1, 0, 32, 16, 16)
TRUCK_POSITION = (0, 109)

#------------------------------------
# ============ PACKAGES =============
#------------------------------------
PACKAGE_SPAWN_INTERVAL = 100

PACKAGE_STEP_SIZE = 8

PACKAGE_1st_SPRITE = (1, 3, 12, 10, 4)
PACKAGE_2nd_SPRITE = (1, 19, 10, 10, 6)
PACKAGE_3rd_SPRITE = (1, 35, 10, 10, 6)
PACKAGE_4th_SPRITE = (1, 51, 8, 10, 8)
PACKAGE_5th_SPRITE = (1, 3, 22, 10, 10)

#------------------------------------
# ============== BOSS ==============
#------------------------------------
BOSS_SPRITE_MARIO = (0, 0, 64, 16, 16)    # Boss looking left (for Mario)
BOSS_SPRITE_LUIGI = (0, 0, 64, -16, 16)   # Boss looking right (for Luigi)

#------------------------------------
# ========== GAME SETTINGS ==========
#------------------------------------
MAX_FAILURES = 3
SCOLDING_DURATION = 180  # Frames (3 seconds at 60 FPS)
