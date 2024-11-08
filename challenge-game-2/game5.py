import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
background_image = pygame.image.load("img/bg2.gif")
player_image = pygame.image.load("img/char.png")
enemy_image = pygame.image.load("img/enemyimg.png")
laser_image = pygame.image.load("img/laser.gif")

# Load explosion animation frames
explosion_frames = [pygame.image.load(f"img/explosion.png") for i in range(1, 6)]

# Scale images (if needed)
player_image = pygame.transform.scale(player_image, (50, 40))
enemy_image = pygame.transform.scale(enemy_image, (50, 40))
laser_image = pygame.transform.scale(laser_image, (5, 20))
explosion_frames = [pygame.transform.scale(frame, (50, 50)) for frame in explosion_frames]

# Player settings
player_width, player_height = 50, 40
player_speed = 4

# Laser settings
laser_speed = 7
burst_shot_count = 3
burst_cooldown = 20

# Enemy settings
enemy_width, enemy_height = 50, 40
enemy_speed = 3
enemy_spawn_delay = 40

# Score and time limit
target_score = 30
time_limit = 60
font = pygame.font.Font(None, 36)

# Background music
pygame.mixer.music.load("img/Kanye West - Heard Em Say (Instrumental).mp3")
pygame.mixer.music.play(-1)

# Game loop control
clock = pygame.time.Clock()

# Explosion class to handle each explosion animation
class Explosion:
    def __init__(self, x, y):
        self.frames = explosion_frames
        self.current_frame = 0
        self.x = x
        self.y = y
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer % 5 == 0:  # Slow down animation speed
            self.current_frame += 1

    def is_finished(self):
        return self.current_frame >= len(self.frames)

    def draw(self):
        if self.current_frame < len(self.frames):
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

# Game functions
def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_laser(laser):
    screen.blit(laser_image, (laser.x, laser.y))

def draw_enemy(enemy):
    screen.blit(enemy_image, (enemy.x, enemy.y))

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_time(remaining_time):
    time_text = font.render(f"Time: {remaining_time}", True, WHITE)
    screen.blit(time_text, (WIDTH - 150, 10))

def show_menu(message):
    screen.fill(BLACK)
    title_text = font.render(message, True, WHITE)
    start_text = font.render("Press ENTER to start", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Main game function
def main_game():
    player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10
    lasers = []
    enemies = []
    explosions = []
    enemy_timer = 0      
    score = 0
    start_ticks = pygame.time.get_ticks()

    burst_timer = 0
    shots_in_burst = 0

    running = True

    while running:
        # Draw background image
        screen.blit(background_image, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate remaining time
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = time_limit - seconds_passed
        if remaining_time <= 0:
            remaining_time = 0

        # Check win/lose conditions
        if score >= target_score:
            show_menu("You Win!")
            return
        if remaining_time == 0:
            if score < target_score:
                show_menu("Game Over! Time's Up")
            return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
            player_y += player_speed

        # Laser burst shooting with cooldown
        if keys[pygame.K_SPACE] and burst_timer == 0 and shots_in_burst < burst_shot_count:
            lasers.append(pygame.Rect(player_x + player_width // 2 - laser_image.get_width() // 2, player_y, laser_image.get_width(), laser_image.get_height()))
            shots_in_burst += 1
            if shots_in_burst >= burst_shot_count:
                burst_timer = burst_cooldown
        if burst_timer > 0:
            burst_timer -= 1
            if burst_timer == 0:
                shots_in_burst = 0

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

        # Collision detection and explosions
        for enemy in enemies[:]:
            for laser in lasers[:]:
                if enemy.colliderect(laser):
                    # Add explosion at enemy location
                    explosions.append(Explosion(enemy.x, enemy.y))
                    enemies.remove(enemy)
                    lasers.remove(laser)
                    score += 1
                    break
            if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                show_menu("Game Over! You were hit.")
                return

        # Update and draw explosions
        for explosion in explosions[:]:
            explosion.update()
            explosion.draw()
            if explosion.is_finished():
                explosions.remove(explosion)

        # Draw everything
        draw_player(player_x, player_y)
        for laser in lasers:
            draw_laser(laser)
        for enemy in enemies:
            draw_enemy(enemy)
        display_score(score)
        display_time(remaining_time)

        pygame.display.flip()
        clock.tick(60)

# Game start
show_menu("Welcome to Space Shooter")
while True:
    main_game()
