import pygame

from .constants import (
    BLUE,
    FOOD_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    WHITE,
)


def create_food(walls):
    """Create food dots in all non-wall tiles that are reachable from Pacman's start position"""
    food = []
    # Grid size based on screen and tile size
    grid_width = SCREEN_WIDTH // TILE_SIZE
    grid_height = SCREEN_HEIGHT // TILE_SIZE

    # Create a set of wall tiles for quick lookup
    wall_tiles = set()
    for wall in walls:
        wx = int(wall[0] // TILE_SIZE)
        wy = int(wall[1] // TILE_SIZE)
        ww = int(wall[2] // TILE_SIZE)
        wh = int(wall[3] // TILE_SIZE)
        for x in range(wx, wx + ww):
            for y in range(wy, wy + wh):
                wall_tiles.add((x, y))

    # Find all reachable tiles from Pacman's starting position using BFS
    start_x = 4  # Pacman starts at tile (4, 10)
    start_y = 10
    reachable_tiles = set()

    # BFS to find all reachable tiles
    queue = [(start_x, start_y)]
    visited = set()
    visited.add((start_x, start_y))

    while queue:
        cx, cy = queue.pop(0)
        reachable_tiles.add((cx, cy))

        # Check all 4 directions
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited and (nx, ny) not in wall_tiles:
                # Check bounds (excluding outer borders)
                if 2 <= nx < grid_width - 2 and 2 <= ny < grid_height - 2:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    # Add food only to reachable non-wall tiles (excluding borders)
    for x in range(2, grid_width - 2):
        for y in range(2, grid_height - 2):
            if (x, y) not in wall_tiles and (x, y) in reachable_tiles:
                food.append(
                    (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                )

    return food


def create_maze():
    # Create maze walls as rectangles (x, y, width, height)
    walls = []

    # Outer borders (moved inward by one tile for playable area)
    walls.append((0, 0, SCREEN_WIDTH, TILE_SIZE))  # Top
    walls.append((0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))  # Bottom
    walls.append((0, 0, TILE_SIZE, SCREEN_HEIGHT))  # Left
    walls.append(
        (24 * TILE_SIZE, 0, TILE_SIZE, SCREEN_HEIGHT)
    )  # Right border (full tile 24)

    # Internal walls - expanded for 25x19 grid
    # Horizontal walls
    for i in range(3, 23, 4):
        walls.append((i * TILE_SIZE, 3 * TILE_SIZE, TILE_SIZE, 4 * TILE_SIZE))
        walls.append((i * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE, 3 * TILE_SIZE))

    # More internal structures
    walls.append((6 * TILE_SIZE, 3 * TILE_SIZE, 14 * TILE_SIZE, TILE_SIZE))
    walls.append((6 * TILE_SIZE, 3 * TILE_SIZE, TILE_SIZE, 5 * TILE_SIZE))
    walls.append((17 * TILE_SIZE, 3 * TILE_SIZE, TILE_SIZE, 5 * TILE_SIZE))
    walls.append((6 * TILE_SIZE, 7 * TILE_SIZE, 2 * TILE_SIZE, 3 * TILE_SIZE))
    walls.append((15 * TILE_SIZE, 7 * TILE_SIZE, 2 * TILE_SIZE, 3 * TILE_SIZE))
    walls.append((9 * TILE_SIZE, 9 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE))

    return walls


def draw_food(screen, food):
    """Draw all food dots"""
    for fx, fy in food:
        pygame.draw.circle(screen, WHITE, (int(fx), int(fy)), FOOD_RADIUS)


def draw_maze(screen, walls):
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)
