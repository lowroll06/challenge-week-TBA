import pygame
import random
import sys

# Kleurdefinities
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialiseer pygame
pygame.init()

# Scherminstellingen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avontuur op het Eiland")

# Laad lettertype
font = pygame.font.Font(None, 36)

# Globale variabelen voor de game state
hp = 100
day = 1
message = "Welkom op het eiland. Wat wil je doen?"
choice_made = False
current_day_action = None

# Functie om tekst weer te geven op het scherm
def draw_text(text, x, y, font, color=BLACK):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Functie om een knop te maken
def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            return action
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + (w // 2 - text_surf.get_width() // 2), y + (h // 2 - text_surf.get_height() // 2)))

# Functie om het spel te resetten
def reset_game():
    global hp, day, message, choice_made
    hp = 100
    day = 1
    message = "Welkom op het eiland. Wat wil je doen?"
    choice_made = False

# Hoofd spelfunctie
def start_game():
    global hp, day, message, choice_made, current_day_action
    
    clock = pygame.time.Clock()
    
    while True:
        screen.fill(WHITE)

        # Tekst voor de dag en HP
        draw_text(f"Dag {day}", 10, 10, font)
        draw_text(f"HP: {hp}", 10, 50, font)

        # Spel logica en keuzes
        if day == 1 and not choice_made:
            draw_text("Je kijkt om je heen. Wat zoek je?", 10, 100, font)
            action = button("1. Hout", 50, 150, 200, 50, GREEN, RED, action="day1_hout")
            action2 = button("2. Eten", 300, 150, 200, 50, GREEN, RED, action="day1_eten")

            if action:
                current_day_action = action
                choice_made = True
            if action2:
                current_day_action = action2
                choice_made = True

        # Dag 1 acties na keuze
        if current_day_action == "day1_hout":
            message = "Je blijft warm en hebt de nacht overleefd. +5 HP"
            hp += 5
            current_day_action = None
            day += 1
            choice_made = False
        elif current_day_action == "day1_eten":
            hp = gather_food(hp)
            day += 1
            choice_made = False
            current_day_action = None

        # Tekstbericht updaten
        draw_text(message, 10, 300, font)

        # Als je hp op is
        if hp <= 0:
            message = "Je HP is op. Je hebt het niet overleefd."
            action = button("Opnieuw proberen", 50, 400, 200, 50, GREEN, RED, action="reset")
            action2 = button("Afsluiten", 300, 400, 200, 50, GREEN, RED, action="exit")

            if action == "reset":
                reset_game()
            if action2 == "exit":
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(30)

# dag 1: Zoek naar eten
def gather_food(hp):
    message = "Je gaat op zoek naar eten. Wat ga je doen?"
    choice_2 = button("1. Bessen verzamelen", 50, 150, 200, 50, GREEN, RED, action="bessen")
    choice_3 = button("2. Jagen", 300, 150, 200, 50, GREEN, RED, action="jagen")

    if choice_2 == "bessen":
        message = "Je vindt bessen, maar ze zijn giftig. -10 HP"
        hp -= 10
    elif choice_3 == "jagen":
        message = "Je hebt een vis gevangen. +10 HP"
        hp += 10

    return hp

# Start het spel
start_game()
