import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Space Shooter")

# Load assets
background_image = pygame.image.load("img/imgbg4.jpg")  # Zorg ervoor dat deze afbeelding bestaat
player_image = pygame.image.load("img/imgchar4.png")  # Zorg ervoor dat deze afbeelding bestaat
enemy_image = pygame.image.load("img/imgchar4.png")  # Zorg ervoor dat deze afbeelding bestaat
pygame.mixer.music.load("img\Kanye West - Heard Em Say (Instrumental).mp3")  # Zorg ervoor dat dit muzieknr bestaat
pygame.mixer.music.play(-1)  # Loopt de muziek door

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width, player_height = 50, 40
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10
player_speed = 4

# Laser settings
laser_width, laser_height = 5, 20
laser_speed = 7
lasers = []

# Enemy settings
enemy_width, enemy_height = 20, 10
enemy_speed = 6
enemies = []
enemy_spawn_delay = 30  # Frames tussen vijand-spawns
enemy_timer = 0

# Timer en score
score = 0
time_limit = 30  # Tijdslimiet in seconden
font = pygame.font.Font(None, 36)

# Game loop control
clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()

# Menu instellingen
menu = True
game_over = False

# Game functies
def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_laser(laser):
    pygame.draw.rect(screen, RED, laser)

def draw_enemy(enemy):
    screen.blit(enemy_image, (enemy.x, enemy.y))

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_timer(remaining_time):
    timer_text = font.render(f"Time: {remaining_time}", True, WHITE)
    screen.blit(timer_text, (WIDTH - 100, 10))

def main_menu():
    screen.fill(BLACK)
    title_text = font.render("Press Enter to Start", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Game loop
while running:
    if menu:
        main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                menu = False
                start_time = pygame.time.get_ticks()  # Reset timer bij start
        continue

    screen.blit(background_image, (0, 0))  # Voeg achtergrond toe

    # Tijd update
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = max(0, time_limit - int(elapsed_time))
    
    if remaining_time <= 0:
        game_over = True if score < 10 else False  # Stel win/verlies voorwaardes in
        menu = True
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:  # Opwaartse beweging
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:  # Neerwaartse beweging
        player_y += player_speed
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
            game_over = True
            menu = True
            break

    # Draw everything
    draw_player(player_x, player_y)
    for laser in lasers:
        draw_laser(laser)
    for enemy in enemies:
        draw_enemy(enemy)
    display_score(score)
    display_timer(remaining_time)

    pygame.display.flip()
    clock.tick(36)

# Sluit de game af
pygame.quit()
sys.exit()
