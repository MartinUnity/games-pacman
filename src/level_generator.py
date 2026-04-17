"""Procedural maze generation for Pacman levels.

Generates mazes using randomized recursive backtracking with:
- Guaranteed reachability (all empty tiles accessible via BFS)
- Wall density capped at ~60%
- Pacman spawn tile always kept clear
"""

import random
from collections import deque

import pygame

from .constants import (
    BLUE,
    FOOD_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    WHITE,
)

# ── Grid dimensions ──────────────────────────────────────────────
GRID_COLS = SCREEN_WIDTH // TILE_SIZE  # 25
GRID_ROWS = SCREEN_HEIGHT // TILE_SIZE  # 19

# Playable area for maze generation (inner grid, excluding 1-tile corridor)
PLAY_LEFT = 2
PLAY_RIGHT = GRID_COLS - 3  # 22
PLAY_TOP = 2
PLAY_BOTTOM = GRID_ROWS - 3  # 16

MAZE_COLS = PLAY_RIGHT - PLAY_LEFT + 1  # 21
MAZE_ROWS = PLAY_BOTTOM - PLAY_TOP + 1  # 15

# Pacman's starting tile in world coordinates
PACMAN_START = (4, 10)


# ── Public API ───────────────────────────────────────────────────


def generate_maze_grid(seed=None):
    """Generate a maze grid via randomized recursive backtracking.

    Returns
    -------
    list[list[int]]
        2-D array where 0 = empty, 1 = wall.  Dimensions are
        (MAZE_ROWS, MAZE_COLS).  Every empty cell is reachable from
        every other empty cell.

    Parameters
    ----------
    seed : int or None
        Optional random seed for reproducible mazes.
    """
    rng = random.Random(seed)
    for _attempt in range(100):
        maze = _carve_maze(MAZE_COLS, MAZE_ROWS, rng)
        _ensure_spawn_open(maze)
        _widen_passages(maze, rng)
        if _verify_reachability(maze) and _check_density(maze):
            return maze
    return _fallback_grid()


def maze_to_walls(maze):
    """Convert a maze grid into a list of wall rectangles.

    The returned list contains:
    1. Four screen-filling border rectangles (top, bottom, left, right).
    2. One merged rectangle per contiguous block of internal walls.

    Each rectangle is ``(x, y, width, height)`` in pixels.
    """
    walls = [
        (0, 0, SCREEN_WIDTH, TILE_SIZE),
        (0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH, TILE_SIZE),
        (0, 0, TILE_SIZE, SCREEN_HEIGHT),
        (SCREEN_WIDTH - TILE_SIZE, 0, TILE_SIZE, SCREEN_HEIGHT),
    ]

    rows, cols = len(maze), len(maze[0])
    visited = set()

    for y in range(rows):
        for x in range(cols):
            if maze[y][x] != 1 or (x, y) in visited:
                continue
            # Extend rightward
            w = 1
            while x + w < cols and maze[y][x + w] == 1 and (x + w, y) not in visited:
                w += 1
            # Extend downward while every column in the run stays walled
            h = 1
            while y + h < rows and all(maze[y + h][x + dx] == 1 for dx in range(w)):
                h += 1
            walls.append(
                (
                    (x + PLAY_LEFT) * TILE_SIZE,
                    (y + PLAY_TOP) * TILE_SIZE,
                    w * TILE_SIZE,
                    h * TILE_SIZE,
                )
            )
            for dy in range(h):
                for dx in range(w):
                    visited.add((x + dx, y + dy))

    return walls


def draw_maze(screen, walls):
    """Draw wall rectangles onto *screen* in BLUE."""
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)


def draw_food(screen, food):
    """Draw food dots onto *screen* in WHITE."""
    for fx, fy in food:
        pygame.draw.circle(screen, WHITE, (int(fx), int(fy)), FOOD_RADIUS)


# ── Maze carving ─────────────────────────────────────────────────


def _carve_maze(cols, rows, rng):
    """Recursive-backtracking maze on odd-indexed cells."""
    grid = [[1] * cols for _ in range(rows)]

    # Seed cells: only odd x / odd y positions
    seed_cells = [
        (gx, gy)
        for gy in range(rows)
        for gx in range(cols)
        if gx % 2 == 1 and gy % 2 == 1
    ]
    if not seed_cells:
        seed_cells = [(cols // 2, rows // 2)]

    sx, sy = rng.choice(seed_cells)
    stack = [(sx, sy)]
    grid[sy][sx] = 0

    while stack:
        cx, cy = stack[-1]
        neighbours = []
        for dx, dy in ((0, -2), (0, 2), (-2, 0), (2, 0)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 1:
                neighbours.append((nx, ny, cx + dx // 2, cy + dy // 2))
        if neighbours:
            nx, ny, px, py = rng.choice(neighbours)
            grid[py][px] = 0  # carve passage
            grid[ny][nx] = 0  # carve cell
            stack.append((nx, ny))
        else:
            stack.pop()

    return grid


def _ensure_spawn_open(grid):
    """Force the tile where Pacman spawns to be empty (0)."""
    gx = PACMAN_START[0] - PLAY_LEFT
    gy = PACMAN_START[1] - PLAY_TOP
    if 0 <= gx < len(grid[0]) and 0 <= gy < len(grid):
        grid[gy][gx] = 0


def _widen_passages(grid, rng):
    """Widen some passages so dead-ends and tight corridors are escapable.

    Strategy
    --------
    1. *Dead-end cells* (exactly 1 empty neighbour) get their connecting
       passage widened by one tile, giving Pacman a side-bay to dodge mobs.
    2. *Junctions* (3+ empty neighbours) are widened with ~20 % probability
       to create small open squares.
    3. A small fraction of widened cells get an additional neighbour carved
       to occasionally produce 3-wide pockets.
    """
    rows, cols = len(grid), len(grid[0])

    def _empty_neighbours(x, y):
        """Count how many of the four orthogonal neighbours are empty."""
        count = 0
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                count += 1
        return count

    # ── 1. Always widen dead-end passages ──────────────────────
    dead_ends = [
        (x, y)
        for y in range(rows)
        for x in range(cols)
        if grid[y][x] == 0 and _empty_neighbours(x, y) == 1
    ]

    for x, y in dead_ends:
        # Find the one empty neighbour (the passage direction)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                # Carve a tile perpendicular to the passage direction
                if dx != 0:  # horizontal passage → widen vertically
                    wy = y - 1 if y > 0 else y + 1
                    wx = x
                else:  # vertical passage → widen horizontally
                    wx = x - 1 if x > 0 else x + 1
                    wy = y
                if 0 <= wx < cols and 0 <= wy < rows and grid[wy][wx] == 1:
                    grid[wy][wx] = 0
                break

    # ── 2. Widen some junctions for open bypass areas ─────────
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0 and _empty_neighbours(x, y) >= 3:
                if rng.random() < 0.20:  # 20 % chance per junction
                    # Carve one perpendicular wall neighbour
                    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 1:
                            grid[ny][nx] = 0
                            # 30 % chance to carve a second neighbour → 3-wide
                            if rng.random() < 0.30:
                                for dx2, dy2 in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                                    nx2, ny2 = nx + dx2, ny + dy2
                                    if (
                                        0 <= nx2 < cols
                                        and 0 <= ny2 < rows
                                        and grid[ny2][nx2] == 1
                                    ):
                                        grid[ny2][nx2] = 0
                                        break
                            break


# ── Invariants ───────────────────────────────────────────────────


def _verify_reachability(grid):
    """BFS from the first empty cell — every empty cell must be visited."""
    rows, cols = len(grid), len(grid[0])
    start = None
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0:
                start = (x, y)
                break
        if start:
            break
    if start is None:
        return False

    visited = {start}
    queue = deque([start])
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < cols
                and 0 <= ny < rows
                and (nx, ny) not in visited
                and grid[ny][nx] == 0
            ):
                visited.add((nx, ny))
                queue.append((nx, ny))

    return all(
        grid[y][x] != 0 or (x, y) in visited for y in range(rows) for x in range(cols)
    )


def _check_density(grid, max_wall_ratio=0.60):
    """Return True when wall proportion does not exceed *max_wall_ratio*."""
    total = sum(len(row) for row in grid)
    walls = sum(cell for row in grid for cell in row)
    return (walls / total) <= max_wall_ratio if total else False


# ── Fallback ─────────────────────────────────────────────────────


def _fallback_grid():
    """Guaranteed-reachable grid with simple horizontal/vertical corridors."""
    cols = MAZE_COLS
    rows = MAZE_ROWS
    grid = [[1] * cols for _ in range(rows)]
    for gy in range(rows):
        for gx in range(cols):
            # Corridors every other row and column
            if gx % 2 == 0 or gy % 2 == 0:
                grid[gy][gx] = 0
    _ensure_spawn_open(grid)
    return grid
