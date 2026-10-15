# Mario Bros Game & Watch

A recreation of the classic *Mario Bros.* Game & Watch handheld game, built in **Python** with the **[Pyxel](https://github.com/kitao/pyxel)** retro game engine. Developed as a university project (Programming, UC3M).

Mario and Luigi work on a packaging line: packages travel along conveyor belts across several floors, and the two brothers have to move between floors to pass them along until they reach the delivery truck. Miss too many and the boss shows up.

<!-- OPTIONAL: add a screenshot or GIF here. Example:
![Gameplay](screenshot.png)
-->

## How to play

| Key | Action |
|-----|--------|
| `W` / `S` | Move Luigi (left side) up / down |
| `↑` / `↓` | Move Mario (right side) up / down |
| `R` | Restart after Game Over |
| `Q` | Quit |

- Every package you deliver adds to your score.
- Dropping a package makes the boss scold you for 3 seconds.
- After **3 failures** it's Game Over.

## Installation

You need [Python 3](https://www.python.org/downloads/) and Pyxel:

```bash
pip install pyxel
```

## Run the game

The game loads its resources using a relative path, so it must be launched **from inside the `Classes` folder**:

```bash
cd Classes
python Main.py
```

## Project structure

```
.
├── resources.pyxres      # Sprites and graphics (Pyxel resource file)
└── Classes/
    ├── Main.py           # Entry point
    ├── Board.py          # Game controller: game loop, scoring, rendering
    ├── Character.py      # Mario and Luigi
    ├── Conveyor.py       # Conveyor belts
    ├── Package.py        # Packages moving through the line
    ├── Truck.py          # Delivery truck
    ├── Boss.py           # The boss and the Game Over logic
    └── constants.py      # Game constants (positions, sprites, settings)
```

The code follows an object-oriented design: `Board` coordinates the game and delegates specific behaviour to `Character`, `Conveyor`, `Package`, `Truck` and `Boss`.

## Tech

- Python
- Pyxel
- Object-oriented programming

## Disclaimer

This is a non-commercial educational fan project. *Mario Bros.* and its characters belong to Nintendo; this project is not affiliated with or endorsed by Nintendo.
