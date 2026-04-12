import sys

import pygame

from .constants import (
    BLACK,
    DOWN,
    FPS,
    HIGHSCORE_FILE,
    LEFT,
    RED,
    RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STOP,
    TILE_SIZE,
    UP,
    WHITE,
    YELLOW,
)
from .game import Game
from .highscore import load_highscore, save_highscore
from .maze import draw_food, draw_maze
from .mob import Mob
from .pacman import Pacman


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
