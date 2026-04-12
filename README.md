# Pacman Game

A classic Pacman-inspired game built with Python and Pygame.

## Features

- **Basic Pacman Movement**: Control Pacman with arrow keys
- **Animated Mouth**: Pacman's mouth opens and closes smoothly
- **Simple Maze**: Blue walls with outer borders and internal structures
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
- **Level 1**: Starting level (no mobs)
- **Level 2**: Added 1x normal mob
- **Level 3**: Added 2x normal mobs
- **Level 4**: Added 3x normal mobs + 1x seeker mob (moves at 25% of player speed)
- **Level 5**: Added 3x normal mobs + 3x seeker mobs
- **Levels 6-9**: Additional levels with increasing difficulty

## Game Details

- **Window Size**: 1024x768 pixels
- **Frame Rate**: 60 FPS
- **Tile System**: 40px tiles (25x19 grid)
- **Pacman**: Yellow circle (8px radius) with animated mouth
- **Mobs**: Red circles that move randomly or chase the player
- **Food**: White dots (3px radius) worth 10 points each
- **Maze**: Blue walls with 40px outer borders

## Technical Implementation

- **Entry Point**: `src/main.py` - `main()` function
- **Development**: Active development in `src/main.py`
- **Archive**: Historical implementation attempts stored in `archive/` (do not edit)

## Running the Game

```bash
python -m src.main
```

Use virtual environment: `.venv/`
