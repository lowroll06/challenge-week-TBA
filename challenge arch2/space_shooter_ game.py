import pygame 
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceload Buster")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
background_image = pygame.image.load("img/bg2.gif")
player_image = pygame.image.load("img/char.png")
enemy_image = pygame.image.load("img/enemyimg.png")
laser_image = pygame.image.load("img/laser.gif")
boss_image = pygame.image.load("img/boss.gif")
boss_explosion_image = pygame.image.load("img/explosionboss.png")
enemy_laser_image = pygame.image.load("img/laserenemy.png")


# Load the boss explosion image
boss_explosion_image = pygame.image.load("img/explosionboss.png").convert()
boss_explosion_image.set_colorkey((255, 255, 255))  # Set white background as transparent

# Load explosion animation frames
explosion_frames = [pygame.image.load(f"img/explosion.png") for i in range(1, 6)]

# Scale images (if needed)
player_image = pygame.transform.scale(player_image, (50, 40))
enemy_image = pygame.transform.scale(enemy_image, (50, 40))
laser_image = pygame.transform.scale(laser_image, (5, 20))
explosion_frames = [pygame.transform.scale(frame, (50, 50)) for frame in explosion_frames]
boss_image = pygame.transform.scale(boss_image, (200, 150))  
enemy_laser_image = pygame.transform.scale(enemy_laser_image, (10, 30))


# Load sound effects
laser_sound = pygame.mixer.Sound("img/lasersound2.mp3")  # Replace with actual path to your sound file
explosion_sound = pygame.mixer.Sound("img/explosionsound2.mp3")  # Replace with actual path to your sound file
laser_sound.set_volume(0.05)  # Set the volume to 20% (0.0 to 1.0)
explosion_sound.set_volume(1.0)  # Set the volume to 20% (0.0 to 1.0)


# Player settings
player_width, player_height = 50, 40
player_speed = 5

# Laser settings
laser_speed = 40
burst_shot_count = 3
burst_cooldown = 17 

# Boss settings
boss_active = False
boss_x, boss_y = WIDTH // 2 - 100, -150
boss_speed = 2  
boss_health = 20
boss_mode = False
# Boss health bar settings
boss_health_bar_width = 200  # Maximum width of the health bar
boss_health_bar_height = 15  # Height of the health bar
boss_health_bar_color = (255, 0, 0)  # Red for the health
boss_health_bar_border_color = WHITE  # Border color

enemy_lasers = []
enemy_laser_speed = 5  # Speed of enemy lasers
enemy_laser_cooldown = 60  # Delay (in frames) between shots

# Enemy settings
enemy_width, enemy_height = 50, 40
enemy_speed = 2
enemy_spawn_delay = 40

# Score and time limit
target_score = 40
time_limit = 120
font = pygame.font.Font(None, 36)

# Background music
pygame.mixer.music.load("img/background3.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)  # Example: 50% volume


def draw_health_bar(x, y, current_health, max_health):
    # Calculate the width of the health bar based on the current health
    current_bar_width = (current_health / max_health) * boss_health_bar_width

    # Draw the health bar
    pygame.draw.rect(screen, boss_health_bar_color, (x, y, current_bar_width, boss_health_bar_height))
    
    # Draw the border of the health bar
    pygame.draw.rect(screen, boss_health_bar_border_color, (x, y, boss_health_bar_width, boss_health_bar_height), 2)


# Game loop control
clock = pygame.time.Clock()

class BossExplosion:
    def __init__(self, x, y):
        self.frames = explosion_frames  # Use the same explosion frames
        self.current_frame = 0
        self.x = x
        self.y = y
        self.timer = 0
        self.scale_factor = 2  # Start with a larger scale
        self.max_scale = 5  # End with a bigger size
        self.scale_speed = 0.2  # Faster scale growth
        self.rotation_angle = 0  # Initial rotation angle
        self.rotation_speed = 10  # Rotation speed per update

    def update(self):
        self.timer += 1
        if self.timer % 3 == 0:  # Slightly faster animation speed
            self.current_frame += 1

        if self.scale_factor < self.max_scale:
            self.scale_factor += self.scale_speed
        else:
            self.scale_factor = self.max_scale

        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360  # Keep rotating

    def is_finished(self):
        return self.current_frame >= len(self.frames)

    def draw(self):
        if self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]

            # Apply scaling
            scaled_frame = pygame.transform.scale(
                frame, 
                (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor))
            )

            # Apply rotation
            rotated_frame = pygame.transform.rotate(scaled_frame, self.rotation_angle)

            # Center the image
            draw_x = self.x - rotated_frame.get_width() // 2
            draw_y = self.y - rotated_frame.get_height() // 2

            # Draw with a fiery tint
            tinted_frame = rotated_frame.copy()
            tinted_frame.fill((255, 100, 100), special_flags=pygame.BLEND_ADD)  # Add a red glow effect
            screen.blit(tinted_frame, (draw_x, draw_y))


# Explosion class to handle each explosion animation
class Explosion:
    def __init__(self, x, y):
        self.frames = explosion_frames
        self.current_frame = 0
        self.x = x
        self.y = y
        self.timer = 0
        self.scale_factor = 1
        self.max_scale = 2
        self.scale_speed = 0.1


    def update(self):
        self.timer += 1
        if self.timer % 5 == 0:  # Slow down animation speed
            self.current_frame += 1
        if self.scale_factor < self.max_scale:
            self.scale_factor += self.scale_speed
        else:
            self.scale_factor = self.max_scale

    def is_finished(self):
        return self.current_frame >= len(self.frames)

    def draw(self):
        if self.current_frame < len(self.frames):
            scaled_frame = pygame.transform.scale(self.frames[self.current_frame],
                                                  (int(self.frames[self.current_frame].get_width() * self.scale_factor),
                                                   int(self.frames[self.current_frame].get_height() * self.scale_factor)))
            screen.blit(scaled_frame, (self.x - scaled_frame.get_width() // 2, self.y - scaled_frame.get_height() // 2))

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
    title_image = pygame.image.load("img/TitleImage.jpg")
    title_text = font.render(message, True, 'Red')
    start_text = font.render("Press Enter", True, 'Green')
    screen.blit(title_image, (0,0))
    screen.blit(title_text,(WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
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

# resets the game
def reset_game():
    global boss_active, boss_mode, boss_health, boss_x, boss_y, score, enemies, explosions, lasers
    boss_active = False
    boss_mode = False
    boss_health = 20
    boss_x, boss_y = WIDTH // 2 - 100, -150
    score = 0
    enemies = []  # Reset enemies to an empty list
    explosions = []  # Reset explosions to an empty list
    lasers = []  # Reset lasers to an empty list


# Main game function
def main_game():
    global boss_active, boss_x, boss_y, boss_health, boss_lasers, boss_laser_timer, boss_laser, boss_mode # Make boss variables global
     # Boss laser settings
    boss_lasers = []  # List to hold all active boss lasers
    boss_laser_speed = 5  # Speed of boss lasers
    boss_laser_timer = 0  # Timer for firing lasers
    boss_laser_interval = 60  # Interval (in frames) between boss laser shots

    laser_speed = 40
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
            reset_game()
            show_menu("You Win!")
            return
        if remaining_time == 0 or boss_health <= 0:
            reset_game()
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
            laser_sound.play()  # Play laser sound when shot
            shots_in_burst += 1
            if shots_in_burst >= burst_shot_count:
                burst_timer = burst_cooldown
        if burst_timer > 0:
            burst_timer -= 1
            if burst_timer == 0:
                shots_in_burst = 0

                # the appearance of the boss and when it should spawn
            global boss_active
        if score >= 30 and not boss_active:
            boss_active = True

        if score == 30 and not boss_mode:
            boss_mode = True
            boss_active = True
            enemies.clear()

        if not boss_mode:
            enemy_timer +=1
            if enemy_timer >= enemy_spawn_delay:
                enemy_x = random.randint(0, WIDTH - enemy_width)
                enemies.append(pygame.Rect(enemy_x, 0, enemy_width, enemy_height))
                enemy_timer = 0

        

        if boss_active:
            boss_y += boss_speed
            if boss_y > 50:
                boss_y = 50
            screen.blit(boss_image, (boss_x, boss_y))

            health_bar_x = boss_x + boss_image.get_width() // 2 - boss_health_bar_width // 2
            health_bar_y = boss_y - boss_health_bar_height - 10
            draw_health_bar(health_bar_x, health_bar_y, boss_health, 10)


            # Boss laser firing
            boss_laser_timer += 1
            if boss_laser_timer >= boss_laser_interval:
                boss_lasers.append(pygame.Rect(
                    boss_x + boss_image.get_width() // 2 - laser_image.get_width() // 2,  # Center the laser
                    boss_y + boss_image.get_height(),  # Start below the boss
                    laser_image.get_width(),
                    laser_image.get_height()
                ))
                boss_laser_timer = 0
            
            # Update and draw boss lasers
            for boss_laser in boss_lasers[:]:
                boss_laser.y += boss_laser_speed
                if boss_laser.y > HEIGHT:  # Remove laser if it moves off-screen
                    boss_lasers.remove(boss_laser)
                else:
                    screen.blit(laser_image, boss_laser)
                # Check for collision with the player
                player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
                if boss_laser.colliderect(player_rect):
                    show_menu("Game Over! You were hit by the boss laser.")
                    return
                    
            boss_rect = pygame.Rect(boss_x, boss_y, boss_image.get_width(), boss_image.get_height())
            for laser in lasers[:]:
                if boss_rect.colliderect(laser):
                    boss_health -= 1  # Reduce boss health
                    lasers.remove(laser)  # Remove the laser
                    if boss_health <= 0:  # If boss is defeated
                        boss_active = False  # Deactivate the boss
                        score += 10  # Reward the player
                        explosions.append(BossExplosion(boss_x + boss_image.get_width() // 2, boss_y + boss_image.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.delay(500)
                        break
        if not boss_active:
            boss_lasers.clear()


        # Update lasers
        for laser in lasers[:]:
            laser.y -= laser_speed
            if laser.y < 0:
                lasers.remove(laser)

        # making the game more difficult when the score gets higher
        if score >= 10:
            enemy_timer +=1.5
            laser_speed = 50

        if score >= 15:
            for enemy in enemies:
                if random.randint(0, 100) < 2:  # 2% chance to shoot per frame
                    enemy_lasers.append(pygame.Rect(
                        enemy.x + enemy.width // 2 - enemy_laser_image.get_width() // 2, 
                        enemy.y + enemy.height, 
                        enemy_laser_image.get_width(), 
                        enemy_laser_image.get_height()
                    ))

        if score >= 20:
            enemy_timer += 2
            laser_speed = 60
        
        for enemy_laser in enemy_lasers[:]:
            enemy_laser.y += enemy_laser_speed
            if enemy_laser.y > HEIGHT:  # Remove off-screen lasers
                enemy_lasers.remove(enemy_laser)
            else:
                screen.blit(enemy_laser_image, (enemy_laser.x, enemy_laser.y))

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for enemy_laser in enemy_lasers:
            if enemy_laser.colliderect(player_rect):
                show_menu("Game Over! You were hit by an enemy laser.")
                return
            
        display_score(score)
        display_time(remaining_time)

        pygame.display.flip()


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
                    explosion_sound.play()  # Play the explosion sound
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
show_menu("Welcome to Spaceload Busters")
while True:
    main_game()
