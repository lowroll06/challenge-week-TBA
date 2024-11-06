import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Variables
GRAVITY = 0.1
BIRD_JUMP = -5
PIPE_GAP = 1 
PIPE_WIDTH = 5
PIPE_SPEED = -100

# Load images
BIRD_IMG = pygame.Surface((34, 24))
BIRD_IMG.fill((255, 255, 0))  # A yellow bird
PIPE_IMG = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
PIPE_IMG.fill((0, 255, 0))    # A green pipe

# Bird class
class Bird:
    def __init__(self):
        self.image = BIRD_IMG
        self.rect = self.image.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.velocity = 3  

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

    def jump(self):
        self.velocity = BIRD_JUMP

# Pipe class
class Pipe:
    def __init__(self, x, height, is_top):
        self.image = PIPE_IMG
        self.rect = self.image.get_rect(topleft=(x, height) if is_top else (x, height + PIPE_GAP))

    def update(self):
        self.rect.x += PIPE_SPEED

    def off_screen(self):
        return self.rect.right < 0

# Create pipes with a gap
def create_pipe():
    height = random.randint(200, SCREEN_HEIGHT - 100 - PIPE_GAP)
    top_pipe = Pipe(SCREEN_WIDTH, height, is_top=True)
    bottom_pipe = Pipe(SCREEN_WIDTH, height, is_top=False) 
    return top_pipe, bottom_pipe

# Main game function
def game():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    running = True
    spawn_pipe = pygame.USEREVENT
    pygame.time.set_timer(spawn_pipe, 1)

    while running:
        SCREEN.fill(WHITE)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if event.type == spawn_pipe:
                pipes.extend(create_pipe())

        # Bird update and drawing
        bird.update()
        SCREEN.blit(bird.image, bird.rect)

        # Pipe update and drawing
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]
        for pipe in pipes:
            pipe.update()
            SCREEN.blit(pipe.image, pipe.rect)

            # Check collision
            if bird.rect.colliderect(pipe.rect):
                running = False

        # Score calculation
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not hasattr(pipe, "passed"):
                score += 1
                pipe.passed = True

        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        # Check if bird falls to the ground or flies off the screen
        if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
            running = False

        pygame.display.flip()
        clock.tick(120  )

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    game()
  