# AGENTS.md

## Project Overview

Pure Python Pacman game using Pygame. No other languages or frameworks.

## Project State

**Current working implementation:** Modular structure in `src/` package

The `archive/` directory contains historical implementation attempts. Do not edit files in `archive/`. Active development should be in the `src/` package.

## Project Structure

```
src/
├── __init__.py       # Package marker
├── main.py           # Entry point: pygame init, game loop, event handling, game_over_screen(), main()
├── constants.py      # Game constants (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE, colors, directions, mob speed, food constants, highscore file path)
├── pacman.py         # Pacman class with movement, collision, and drawing
├── mob.py            # Mob class with random/chaser movement, collision, and drawing
├── maze.py           # create_maze(), create_food(), draw_maze(), draw_food()
├── game.py           # Game class with level management
└── highscore.py      # load_highscore(), save_highscore()
```

## Setup & Run

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python -m src.main
```

Use `.venv/` virtual environment (not `venv/`)

## Game Architecture

- **Window:** 1024x768 pixels, 60 FPS
- **Tile system:** TILE_SIZE=40, Pacman/mobs move in grid-aligned tiles (25x19 grid)
- **Pacman:** Yellow circle (radius=8px = TILE_SIZE//2 - 12), speed=2, animated mouth
- **Mobs:** Red circles, speed=2, random movement; Level 4+ adds pink chaser (speed=1)
- **Maze:** Blue walls, 40px outer borders (occupies tiles 0 and 24/18), internal grid-based structures
- **Food:** White dots (radius=3px), score=10 each
- **Highscore:** Persisted to `highscore.txt` in project root, displayed during gameplay and on game over screen

## Controls

- **Arrow keys:** Move Pacman (Up/Down/Left/Right)
- **ESC:** Quit
- **Keys 2-9:** Cheat - jump to specific level

## Entry Point

`src/main.py` - `main()` function

## Guidelines

- **Do not edit `archive/` files** - these are historical snapshots
- Edit files in the `src/` package for active development
- Use relative imports within the `src` package (e.g., `from .constants import TILE_SIZE`)
