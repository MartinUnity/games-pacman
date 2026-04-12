import json
import math
import os
import random
import sys

import pygame

# Game constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TILE_SIZE = 40

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Mob constants
MOB_SPEED = 2  # Half of Pacman's speed (3)

# Food constants
FOOD_RADIUS = 3
FOOD_SCORE = 10

# Highscore file
HIGHSCORE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "highscore.txt"
)


def load_highscore():
    """Load highscore from file, returns 0 if file doesn't exist"""
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                score = int(f.read().strip())
                return score
    except (ValueError, IOError):
        pass
    return 0


def save_highscore(score):
    """Save highscore to file"""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except IOError:
        pass


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


class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.walls = []
        self.food = []
        self.food_remaining = 0
        self.mobs = []

    def reset_level(self):
        self.walls = create_maze()
        self.food = create_food(self.walls)
        self.food_remaining = len(self.food)
        # Place mobs based on level
        self.mobs = []
        # Always place one mob in bottom right corner (tile 23, 17)
        self.mobs.append(
            Mob(23 * TILE_SIZE + TILE_SIZE // 2, 17 * TILE_SIZE + TILE_SIZE // 2)
        )
        # At level 2 and above, add a second mob in bottom left corner (tile 3, 17)
        if self.level >= 2:
            self.mobs.append(
                Mob(3 * TILE_SIZE + TILE_SIZE // 2, 17 * TILE_SIZE + TILE_SIZE // 2)
            )
        # At level 4 and above, add a chaser mob at top right corner (tile 23, 2) at 25% speed
        if self.level >= 4:
            self.mobs.append(
                Mob(
                    23 * TILE_SIZE + TILE_SIZE // 2,
                    2 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,  # 1 pixel per frame (25% of Pacman's speed of 4 tiles/60 frames)
                    is_chaser=True,
                    color=(255, 192, 203),  # Pink color for chaser
                )
            )
        # At level 5 and above, add two more chaser mobs at top left (tile 3, 2) and bottom right (tile 23, 17)
        if self.level >= 5:
            self.mobs.append(
                Mob(
                    3 * TILE_SIZE + TILE_SIZE // 2,
                    2 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
            self.mobs.append(
                Mob(
                    23 * TILE_SIZE + TILE_SIZE // 2,
                    17 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )

    def eat_food(self, x, y):
        # Check if Pacman is close enough to any food to eat it
        eaten = False
        for food in self.food[:]:
            fx, fy = food
            distance = ((x - fx) ** 2 + (y - fy) ** 2) ** 0.5
            if distance < FOOD_RADIUS + 5:
                self.food.remove(food)
                self.score += FOOD_SCORE
                self.food_remaining -= 1
                eaten = True
        return eaten

    def check_level_complete(self):
        return self.food_remaining <= 0


class Mob:
    def __init__(self, x, y, speed=None, is_chaser=False, color=RED):
        self.x = x
        self.y = y
        self.radius = TILE_SIZE // 2 - 12
        self.speed = speed if speed is not None else MOB_SPEED
        self.direction = STOP
        self.change_direction_delay = 0
        self.is_chaser = is_chaser
        self.color = color

    def update(self, walls, pacman_x=None, pacman_y=None):
        # If this is a chaser mob, target Pacman
        if self.is_chaser and pacman_x is not None and pacman_y is not None:
            self._target_pacman(pacman_x, pacman_y, walls)
        else:
            # Random movement pattern
            self.change_direction_delay -= 1
            if self.change_direction_delay <= 0:
                self._pick_random_direction(walls)

        # Try to move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed

        if not self._check_collision(new_x, new_y, walls):
            self.x = new_x
            self.y = new_y
        else:
            # Hit a wall: snap to tile center and pick new direction
            current_tile_x = int(self.x // TILE_SIZE)
            current_tile_y = int(self.y // TILE_SIZE)
            self.x = current_tile_x * TILE_SIZE + TILE_SIZE // 2
            self.y = current_tile_y * TILE_SIZE + TILE_SIZE // 2

            if not self.is_chaser:
                self._pick_random_direction(walls)
            else:
                self._target_pacman(pacman_x, pacman_y, walls)

    def _pick_random_direction(self, walls):
        directions = [UP, DOWN, LEFT, RIGHT]
        random.shuffle(directions)

        for direction in directions:
            if self._can_move(direction, walls):
                self.direction = direction
                self.change_direction_delay = 15 + random.randint(
                    0, 15
                )  # Change direction every 15-30 frames
                break

    def _target_pacman(self, pacman_x, pacman_y, walls):
        """Choose direction that moves toward Pacman"""
        directions = [UP, DOWN, LEFT, RIGHT]

        # Sort directions by distance to Pacman
        def distance_after_move(direction):
            next_x = self.x + direction[0] * self.speed
            next_y = self.y + direction[1] * self.speed
            return (next_x - pacman_x) ** 2 + (next_y - pacman_y) ** 2

        # Try to move in each direction, preferring those that get closer
        sorted_directions = sorted(directions, key=distance_after_move)

        for direction in sorted_directions:
            if self._can_move(direction, walls):
                self.direction = direction
                self.change_direction_delay = 5 + random.randint(
                    0, 5
                )  # More frequent updates for chaser
                break

    def _can_move(self, direction, walls):
        next_x = self.x + direction[0] * self.speed
        next_y = self.y + direction[1] * self.speed
        return not self._check_collision(next_x, next_y, walls)

    def _check_collision(self, x, y, walls):
        radius = self.radius
        for wall in walls:
            # Use inclusive comparisons so touching counts as collision
            if (
                x + radius >= wall[0]
                and x - radius <= wall[0] + wall[2]
                and y + radius >= wall[1]
                and y - radius <= wall[1] + wall[3]
            ):
                return True
        # Screen boundaries: touching the edge is a collision
        if (
            x - radius <= 0
            or x + radius >= SCREEN_WIDTH
            or y - radius <= 0
            or y + radius >= SCREEN_HEIGHT
        ):
            return True
        return False

    def check_mob_collision(self, pacman_x, pacman_y):
        """Check if mob collides with Pacman"""
        distance = ((pacman_x - self.x) ** 2 + (pacman_y - self.y) ** 2) ** 0.5
        return distance < self.radius + TILE_SIZE // 2 - 2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = TILE_SIZE // 2 - 12
        self.direction = STOP
        self.next_direction = STOP
        self.speed = 2
        self.mouth_angle = 0
        self.mouth_opening = True
        self.mouth_speed = 0.15

    def update(self, walls):
        # Try to change direction when aligned with grid
        if self.next_direction != STOP:
            if self._is_aligned_with_grid():
                self._try_change_direction(walls)

        # Move in current direction if valid
        if self.direction != STOP:
            new_x = self.x + self.direction[0] * self.speed
            new_y = self.y + self.direction[1] * self.speed

            if not self._check_collision(new_x, new_y, walls):
                self.x = new_x
                self.y = new_y
            else:
                # Hit a wall: snap to tile center and stop
                current_tile_x = int(self.x // TILE_SIZE)
                current_tile_y = int(self.y // TILE_SIZE)
                self.x = current_tile_x * TILE_SIZE + TILE_SIZE // 2
                self.y = current_tile_y * TILE_SIZE + TILE_SIZE // 2
                self.direction = STOP

        # Update mouth animation
        if self.mouth_opening:
            self.mouth_angle += self.mouth_speed
            if self.mouth_angle >= math.pi / 4:
                self.mouth_opening = False
        else:
            self.mouth_angle -= self.mouth_speed
            if self.mouth_angle <= 0:
                self.mouth_opening = True

    def _is_aligned_with_grid(self):
        # Check if Pacman is close to the center of a tile
        center_x = self.x % TILE_SIZE
        center_y = self.y % TILE_SIZE
        return (
            abs(center_x - TILE_SIZE // 2) <= self.speed
            and abs(center_y - TILE_SIZE // 2) <= self.speed
        )

    def _try_change_direction(self, walls):
        # Get current tile position
        current_tile_x = int(self.x // TILE_SIZE)
        current_tile_y = int(self.y // TILE_SIZE)

        # Check if the next tile in the desired direction is valid
        next_tile_x = current_tile_x + self.next_direction[0]
        next_tile_y = current_tile_y + self.next_direction[1]

        # Only change direction if it's different from current
        if self.next_direction != self.direction:
            if not self._is_wall(next_tile_x, next_tile_y, walls):
                self.direction = self.next_direction
                # Snap to grid center
                self.x = current_tile_x * TILE_SIZE + TILE_SIZE // 2
                self.y = current_tile_y * TILE_SIZE + TILE_SIZE // 2

    def _check_collision(self, x, y, walls):
        # Check if the position overlaps with any wall (using inclusive comparisons)
        radius = self.radius
        for wall in walls:
            if (
                x + radius >= wall[0]
                and x - radius <= wall[0] + wall[2]
                and y + radius >= wall[1]
                and y - radius <= wall[1] + wall[3]
            ):
                return True
        # Check screen boundaries (inclusive)
        if (
            x - radius <= 0
            or x + radius >= SCREEN_WIDTH
            or y - radius <= 0
            or y + radius >= SCREEN_HEIGHT
        ):
            return True
        return False

    def _is_wall(self, tile_x, tile_y, walls):
        # Check if a tile position is a wall
        for wall in walls:
            wall_tile_x = int(wall[0] // TILE_SIZE)
            wall_tile_y = int(wall[1] // TILE_SIZE)
            wall_width_tiles = int(wall[2] // TILE_SIZE)
            wall_height_tiles = int(wall[3] // TILE_SIZE)

            if (
                wall_tile_x <= tile_x < wall_tile_x + wall_width_tiles
                and wall_tile_y <= tile_y < wall_tile_y + wall_height_tiles
            ):
                return True
        return False

    def draw(self, screen):
        # Calculate rotation angle based on direction
        if self.direction == RIGHT:
            angle = 0
        elif self.direction == DOWN:
            angle = math.pi / 2
        elif self.direction == LEFT:
            angle = math.pi
        elif self.direction == UP:
            angle = -math.pi / 2
        else:
            angle = 0

        mouth_start = angle + self.mouth_angle
        mouth_end = angle + (2 * math.pi - self.mouth_angle)

        # Draw Pacman as a pie slice
        points = [(self.x, self.y)]
        for i in range(100):
            theta = mouth_start + (mouth_end - mouth_start) * i / 99
            px = self.x + self.radius * math.cos(theta)
            py = self.y + self.radius * math.sin(theta)
            points.append((px, py))

        pygame.draw.polygon(screen, YELLOW, points)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius, 0)


def draw_food(screen, food):
    """Draw all food dots"""
    for fx, fy in food:
        pygame.draw.circle(screen, WHITE, (int(fx), int(fy)), FOOD_RADIUS)


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


def draw_maze(screen, walls):
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)


def game_over_screen(screen, score):
    """Display game over screen with final score"""
    highscore = load_highscore()

    # Update highscore if current score is higher
    if score > highscore:
        save_highscore(score)
        highscore = score
        new_highscore = True
    else:
        new_highscore = False

    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    highscore_text = font.render(f"High Score: {highscore}", True, YELLOW)

    if new_highscore:
        new_record_text = pygame.font.Font(None, 36).render(
            "NEW HIGH SCORE!", True, YELLOW
        )

    screen.fill(BLACK)
    screen.blit(
        game_over_text,
        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100),
    )
    screen.blit(
        score_text,
        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20),
    )
    screen.blit(
        highscore_text,
        (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60),
    )

    if new_highscore:
        screen.blit(
            new_record_text,
            (
                SCREEN_WIDTH // 2 - new_record_text.get_width() // 2,
                SCREEN_HEIGHT // 2 + 20,
            ),
        )

    pygame.display.flip()

    # Wait for key press or timeout
    pygame.time.wait(2000)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()

    running = True
    while running:
        # Initialize game
        game = Game()
        game.reset_level()

        # Create Pacman
        pacman = Pacman(4 * TILE_SIZE + TILE_SIZE // 2, 10 * TILE_SIZE + TILE_SIZE // 2)

        # Load highscore
        highscore = load_highscore()

        level_running = True
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    level_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        level_running = False
                        running = False
                    elif event.key == pygame.K_UP:
                        pacman.next_direction = UP
                    elif event.key == pygame.K_DOWN:
                        pacman.next_direction = DOWN
                    elif event.key == pygame.K_LEFT:
                        pacman.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT:
                        pacman.next_direction = RIGHT
                    # Cheat keys 2-9 to jump to specific levels
                    elif pygame.K_2 <= event.key <= pygame.K_9:
                        level_num = event.key - pygame.K_0
                        game.level = level_num
                        game.reset_level()
                        # Reset Pacman position
                        pacman.x = 4 * TILE_SIZE + TILE_SIZE // 2
                        pacman.y = 10 * TILE_SIZE + TILE_SIZE // 2
                        pacman.direction = STOP
                        pacman.next_direction = STOP

            # Update game state
            pacman.update(game.walls)
            for mob in game.mobs:
                mob.update(game.walls, pacman.x, pacman.y)

            # Check for food collisions
            game.eat_food(pacman.x, pacman.y)

            # Check if level is complete
            if game.check_level_complete():
                game.level += 1
                game.reset_level()
                # Reset Pacman position
                pacman.x = 4 * TILE_SIZE + TILE_SIZE // 2
                pacman.y = 10 * TILE_SIZE + TILE_SIZE // 2
                pacman.direction = STOP
                pacman.next_direction = STOP

            # Check for mob collision (game over)
            for mob in game.mobs:
                if mob.check_mob_collision(pacman.x, pacman.y):
                    level_running = False
                    game_over_screen(screen, game.score)
                    break

            # Draw everything
            screen.fill(BLACK)
            draw_maze(screen, game.walls)
            draw_food(screen, game.food)
            pacman.draw(screen)
            for mob in game.mobs:
                mob.draw(screen)

            # Draw score, level, and highscore
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {game.score}", True, WHITE)
            level_text = font.render(f"Level: {game.level}", True, WHITE)
            highscore_text = font.render(f"High Score: {highscore}", True, YELLOW)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
            screen.blit(highscore_text, (10, 90))

            pygame.display.flip()

            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
