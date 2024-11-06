import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Movement")

# Colors
WHITE = (12, 150, 15)
BLUE = (98, 30, 189)

# Character settings
character_pos = [WIDTH // 7, HEIGHT // 2]
character_size = 50
character_speed = 4

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Update character position based on key presses
    if keys[pygame.K_LEFT]:
        character_pos[0] -= character_speed
    if keys[pygame.K_RIGHT]:
        character_pos[0] += character_speed
    if keys[pygame.K_UP]:
        character_pos[1] -= character_speed
    if keys[pygame.K_DOWN]:
        character_pos[1] += character_speed

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the character (as a blue rectangle)
    pygame.draw.rect(screen, BLUE, (character_pos[0], character_pos[1], character_size, character_size))

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
