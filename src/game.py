from .constants import FOOD_RADIUS, FOOD_SCORE, TILE_SIZE
from .maze import create_food, create_maze
from .mob import Mob


class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.walls = []
        self.food = []
        self.food_remaining = 0
        self.mobs = []

    def spawn_pos(self):
        """Return (tile_x, tile_y) for Pacman's spawn point."""
        if self.level == 10:
            return (12, 9)
        return (4, 10)

    def reset_level(self):
        self.walls = create_maze(max_wall_ratio=0.62 if self.level == 10 else 0.60, spawn_tile=self.spawn_pos())
        self.food = create_food(self.walls, spawn_tile=self.spawn_pos())
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
        # At level 4+, add a chaser mob at top right corner (tile 23, 2) at 25% speed
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

        # At level 6+, add a third chaser at middle top (tile 13, 2)
        if self.level >= 6:
            self.mobs.append(
                Mob(
                    13 * TILE_SIZE + TILE_SIZE // 2,
                    2 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
        # At level 7+, add a third chaser at middle center (tile 13, 9)
        if self.level >= 7:
            self.mobs.append(
                Mob(
                    13 * TILE_SIZE + TILE_SIZE // 2,
                    9 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
        # At level 8+, add two more chasers at middle bottom (13, 17) and left center (3, 9)
        if self.level >= 8:
            self.mobs.append(
                Mob(
                    13 * TILE_SIZE + TILE_SIZE // 2,
                    17 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
            self.mobs.append(
                Mob(
                    3 * TILE_SIZE + TILE_SIZE // 2,
                    9 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
        # At level 9+, add three more chasers at right center (23, 9), bottom left (3, 17), and middle bottom (13, 17)
        if self.level >= 9:
            self.mobs.append(
                Mob(
                    23 * TILE_SIZE + TILE_SIZE // 2,
                    9 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
            self.mobs.append(
                Mob(
                    3 * TILE_SIZE + TILE_SIZE // 2,
                    17 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
                )
            )
            self.mobs.append(
                Mob(
                    13 * TILE_SIZE + TILE_SIZE // 2,
                    17 * TILE_SIZE + TILE_SIZE // 2,
                    speed=1,
                    is_chaser=True,
                    color=(255, 192, 203),
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

        # At level 7+, add a third normal mob at middle top (tile 13, 2)
        if self.level >= 7:
            self.mobs.append(
                Mob(13 * TILE_SIZE + TILE_SIZE // 2, 2 * TILE_SIZE + TILE_SIZE // 2)
            )
        # At level 8+, add two more normal mobs at middle center (13, 9) and right center (23, 9)
        if self.level >= 8:
            self.mobs.append(
                Mob(13 * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE + TILE_SIZE // 2)
            )
            self.mobs.append(
                Mob(23 * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE + TILE_SIZE // 2)
            )
        # At level 9+, add three more normal mobs at left center (3, 9), middle bottom (13, 17), and bottom left (3, 17)
        if self.level >= 9:
            self.mobs.append(
                Mob(3 * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE + TILE_SIZE // 2)
            )
            self.mobs.append(
                Mob(13 * TILE_SIZE + TILE_SIZE // 2, 17 * TILE_SIZE + TILE_SIZE // 2)
            )
            self.mobs.append(
                Mob(3 * TILE_SIZE + TILE_SIZE // 2, 17 * TILE_SIZE + TILE_SIZE // 2)
            )
        # Level 10: two fast chasers (speed=2, orange) that can match Pacman's speed
        if self.level == 10:
            self.mobs.append(
                Mob(
                    23 * TILE_SIZE + TILE_SIZE // 2,
                    2 * TILE_SIZE + TILE_SIZE // 2,
                    speed=2,
                    is_chaser=True,
                    color=(255, 165, 0),
                )
            )
            self.mobs.append(
                Mob(
                    3 * TILE_SIZE + TILE_SIZE // 2,
                    2 * TILE_SIZE + TILE_SIZE // 2,
                    speed=2,
                    is_chaser=True,
                    color=(255, 165, 0),
                )
            )

        # Ensure no mob is too close to Pacman's spawn point (at least 3 tiles away)
        spawn_x, spawn_y = self.spawn_pos()
        for mob in self.mobs:
            mob_tile_x = mob.x // TILE_SIZE
            mob_tile_y = mob.y // TILE_SIZE
            if abs(mob_tile_x - spawn_x) + abs(mob_tile_y - spawn_y) < 3:
                # Push mob away from spawn
                dx = mob_tile_x - spawn_x
                dy = mob_tile_y - spawn_y
                if abs(dx) >= abs(dy):
                    mob_tile_x += 4 if dx >= 0 else -4
                else:
                    mob_tile_y += 4 if dy >= 0 else -4
                # Clamp to valid range
                mob_tile_x = max(2, min(22, mob_tile_x))
                mob_tile_y = max(2, min(16, mob_tile_y))
                mob.x = mob_tile_x * TILE_SIZE + TILE_SIZE // 2
                mob.y = mob_tile_y * TILE_SIZE + TILE_SIZE // 2

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
