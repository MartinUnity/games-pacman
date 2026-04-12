# AGENTS.md

## Project Overview

Pure Python Pacman game using Pygame. No other languages or frameworks.

## Project State

**Current working implementation:** `src/main.py` (copy of archive/src4/main.py)

The `archive/` directory contains historical implementation attempts. Do not edit files in `archive/`. Active development should be in `src/main.py`.

## Setup & Run

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python src/main.py
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

`src/main.py:549` - `main()` function

## Recent Changes (Current Session)

- **Right wall vibration fix**: Modified Pacman's wall collision response to only align to perpendicular axis instead of snapping to tile center
  - Moving UP/DOWN: align X to grid center, keep Y position
  - Moving LEFT/RIGHT: align Y to grid center, keep X position
  - Prevents oscillation between grid center and wall collision point

## Guidelines

- **Do not edit `archive/` files** - these are historical snapshots
- Edit `src/main.py` for active development
