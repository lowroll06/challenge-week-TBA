import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Voeg toe dat je kan rondvliegen, boven en beneden
# Voeg fotos en achtergrond toe
# Voeg achtergond muziek toe
# voeg een menu toe
# Voeg een timer toe waarbij je een bepaalt aantal punten
# moet halen in een stuk tijd, als je het niet haalt, 
# game over scherm,als je het wel haalt, Win scherm.


# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Space Shooter")

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width, player_height = 50, 40
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10
player_speed = 8

# Laser settings
laser_width, laser_height = 5, 20
laser_speed = 7
lasers = []

# Enemy settings
enemy_width, enemy_height = 50, 40
enemy_speed = 6
enemies = []
enemy_spawn_delay = 40  # Frames between enemy spawns
enemy_timer = 0

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop control
clock = pygame.time.Clock()
running = True

# Game functions
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))

def draw_laser(laser):
    pygame.draw.rect(screen, RED, laser)

def draw_enemy(enemy):
    pygame.draw.rect(screen, WHITE, enemy)

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game loop
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:  # Shoot laser
        lasers.append(pygame.Rect(player_x + player_width // 2 - laser_width // 2, player_y, laser_width, laser_height))

    # Update lasers
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < 0:
            lasers.remove(laser)

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_delay:
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemies.append(pygame.Rect(enemy_x, 0, enemy_width, enemy_height))
        enemy_timer = 0

    # Update enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    # Collision detection
    for enemy in enemies[:]:
        for laser in lasers[:]:
            if enemy.colliderect(laser):
                enemies.remove(enemy)
                lasers.remove(laser)
                score += 1
                break
        if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            running = False  # End game if enemy hits player

    # Draw everything
    draw_player(player_x, player_y)
    for laser in lasers:
        draw_laser(laser)
    for enemy in enemies:
        draw_enemy(enemy)
    display_score(score)

    pygame.display.flip()
    clock.tick(60)

# End the game
pygame.quit()
sys.exit()
