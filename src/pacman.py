import math

import pygame

from .constants import (
    DOWN,
    LEFT,
    PACMAN_RADIUS,
    RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STOP,
    TILE_SIZE,
    UP,
    YELLOW,
)


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PACMAN_RADIUS
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
