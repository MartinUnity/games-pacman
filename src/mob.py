import math
import random

import pygame

from .constants import (
    DOWN,
    LEFT,
    RED,
    RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STOP,
    TILE_SIZE,
    UP,
    MOB_SPEED,
)


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
