# Pacman Game

A classic Pacman-inspired game built with Python and Pygame.

## Features

- **Basic Pacman Movement**: Control Pacman with arrow keys
- **Animated Mouth**: Pacman's mouth opens and closes smoothly
- **Dynamic Maze Generation**: Procedurally generated mazes using recursive backtracking algorithm
- **Guaranteed Playability**: All empty tiles are reachable (verified via BFS); wall density capped at 60%
- **Unique Levels**: Each level generates a fresh maze layout for replayability
- **Smooth Gameplay**: 60 FPS gameplay loop
- **Progressive Difficulty**: Multiple levels with increasing mob counts
- **Cheat Keys**: Instant level testing with keys 2-9

## Installation

```bash
pip install -r requirements.txt
```

## How to Play

### Movement Controls
- **Arrow Keys**: Move Pacman (Up, Down, Left, Right)
- **ESC**: Quit the game

### Cheat Keys (Testing)
- **Keys 2-9**: Instantly jump to a specific level to test implementation

### Level Progression
- **Level 1**: Starting level (1 normal mob)
- **Level 2**: 2 normal mobs
- **Level 3**: 2 normal mobs
- **Level 4**: 2 normal mobs + 1 seeker mob (moves at 25% of player speed)
- **Level 5**: 2 normal mobs + 2 seeker mobs
- **Level 6**: 2 normal mobs + 3 seeker mobs
- **Level 7**: 3 normal mobs + 3 seeker mobs
- **Level 8**: 4 normal mobs + 4 seeker mobs
- **Level 9**: 5 normal mobs + 5 seeker mobs

## Game Details

- **Window Size**: 1024x768 pixels
- **Frame Rate**: 60 FPS
- **Tile System**: 40px tiles (25x19 grid)
- **Pacman**: Yellow circle (8px radius) with animated mouth
- **Mobs**: Red circles that move randomly or chase the player
- **Food**: White dots (3px radius) worth 10 points each
- **Maze**: Procedurally generated each level using recursive backtracking; blue walls, 40px outer borders (occupies tiles 0 and 24/18), internal grid-based structures; walls ≤ 60% of area with all empty tiles reachable

## Technical Implementation

- **Entry Point**: `src/main.py` - `main()` function
- **Development**: Active development in `src/main.py`
- **Archive**: Historical implementation attempts stored in `archive/` (do not edit)

## Running the Game

```bash
python -m src.main
```

Use virtual environment: `.venv/`
