import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shipwreck Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Load assets
background_images = [
    pygame.transform.scale(pygame.image.load("img/dag1img.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/dag2img.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/dag3img.jpg"), (WIDTH, HEIGHT))
]
pygame.mixer.music.load("img/track.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop the music

# Game variables
player_hp = 100
day = 1
game_over = False
font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 36)

# Intro Message
intro_message = "You've survived a cruise ship crash and are stranded on a deserted island."

# Choices for each day
choices_per_day = {
    1: [
        ("Search the beach for supplies (low risk, gain items)", "safe"),
        ("Explore the forest (high risk, find resources or encounter danger)", "risky"),
        ("Build a shelter for the night (gain HP if successful)", "safe"),
    ],
    2: [
        ("Explore a nearby cave (find rare items, risk injury)", "risky"),
        ("Signal for help with a large fire (increases rescue chance)", "safe"),
        ("Search for fresh water (gain HP if successful)", "safe"),
    ],
    3: [
        ("Attempt to swim to a nearby island (risk drowning)", "risky"),
        ("Climb a mountain to signal a plane (gain HP if successful)", "safe"),
        ("Search the wreckage for useful items (find items or risk injury)", "risky"),
    ]
}

# Helper functions
def risky_action():
    return random.choice(["gain_hp", "lose_hp", "item_found", "nothing"])

def safe_action():
    return random.choice(["gain_hp", "item_found", "nothing"])

def resolve_choice(risk_level):
    global player_hp, game_over
    outcome = risky_action() if risk_level == "risky" else safe_action()
    
    if outcome == "gain_hp":
        gained_hp = random.randint(5, 20)
        player_hp = min(100, player_hp + gained_hp)
        return f"You gained {gained_hp} HP!"
    elif outcome == "lose_hp":
        lost_hp = random.randint(10, 30)
        player_hp -= lost_hp
        if player_hp <= 0:
            game_over = True
            return "You were injured and lost HP. Game Over!"
        return f"You were injured and lost {lost_hp} HP."
    elif outcome == "item_found":
        return "You found useful supplies!"
    else:
        return "Nothing happened."

# Main game loop
while not game_over:
    screen.blit(background_images[day - 1], (0, 0))  # Draw background for the current day
    
    # Game progression
    choices = choices_per_day.get(day, [])
    
    # Display game status
    day_text = large_font.render(f"Day {day}", True, BLACK)
    hp_text = large_font.render(f"HP: {player_hp}", True, BLACK)
    intro_text = font.render(intro_message, True, BLACK)
    screen.blit(day_text, (10, 10))
    screen.blit(hp_text, (WIDTH - 100, 10))
    screen.blit(intro_text, (10, 50))

    # Display choices
    for idx, (choice_text, choice_type) in enumerate(choices):
        choice_display = font.render(f"{idx + 1}. {choice_text}", True, BLACK)
        screen.blit(choice_display, (10, 100 + idx * 40))

    pygame.display.flip()

    # Wait for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            choice_outcome = ""
            if event.key == pygame.K_1:
                choice_outcome = resolve_choice(choices[0][1])
            elif event.key == pygame.K_2:
                choice_outcome = resolve_choice(choices[1][1])
            elif event.key == pygame.K_3:
                choice_outcome = resolve_choice(choices[2][1])
            else:
                choice_outcome = "Invalid choice. Choose 1, 2, or 3."

            # Display outcome of choice
            screen.blit(background_images[day - 1], (0, 0))  # Redraw background
            outcome_display = large_font.render(choice_outcome, True, RED if "lost" in choice_outcome else GREEN)
            screen.blit(outcome_display, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)

            # Move to the next day if not game over
            if not game_over:
                day += 1
                if day > 3:
                    # Winning condition
                    screen.blit(background_images[-1], (0, 0))
                    win_text = large_font.render("You survived and were rescued!", True, GREEN)
                    screen.blit(win_text, (WIDTH // 4, HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    game_over = True
