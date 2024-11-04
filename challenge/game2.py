import pygame
import sys
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Adventure Game")
font = pygame.font.Font(None, 36)

# Load images (e.g., background images for each day)
backgrounds = {
    "day1": pygame.image.load("img/dag1img.jpg"),
    "day2": pygame.image.load("img/dag2img.jpg"),
    "day3": pygame.image.load("img/dag3img.jpg")
}

# Set up color
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game variables
hp = 100
day = 1
max_days = 3
door_choice = None
tribe_choice = None

# Utility to draw text
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Button class for clickable choices
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        draw_text(self.text, self.rect.x + 10, self.rect.y + 10)

    def click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# Scene functions
def start_day1():
    global hp
    screen.blit(backgrounds["day1"], (0, 0))
    draw_text("It's Day 1. Choose your action:", 20, 20)
    draw_text(f"HP: {hp}", 20, 60)
    Button("Gather Wood", 100, 200, 200, 50, RED, action=gather_wood).draw()
    Button("Look for Food", 400, 200, 200, 50, RED, action=gather_food).draw()

def gather_wood():
    global hp, day
    hp += 5
    draw_text("You gathered wood and survived the night. +5 HP", 20, 100)
    pygame.display.flip()
    pygame.time.delay(1000)
    day += 1

def gather_food():
    global hp, day
    hp -= 10
    draw_text("You tried to find food, but it was scarce. -10 HP", 20, 100)
    pygame.display.flip()
    pygame.time.delay(1000)
    day += 1

def day2():
    global hp
    screen.blit(backgrounds["day2"], (0, 0))
    draw_text("It's Day 2. Do you explore the East or West?", 20, 20)
    Button("Go East", 100, 200, 200, 50, RED, action=go_east).draw()
    Button("Go West", 400, 200, 200, 50, RED, action=go_west).draw()

def go_east():
    global hp, door_choice
    hp -= 15
    draw_text("You find a strange object but lose HP due to exhaustion.", 20, 100)
    pygame.display.flip()
    pygame.time.delay(1000)
    door_choice = "left"
    
def go_west():
    global hp, tribe_choice
    hp += 10
    draw_text("You met a friendly tribe who helped you rest. +10 HP", 20, 100)
    pygame.display.flip()
    pygame.time.delay(1000)
    tribe_choice = "peaceful"

def day3():
    screen.blit(backgrounds["day3"], (0, 0))
    if door_choice == "left":
        draw_text("You set up a help signal and are rescued!", 20, 100)
    elif tribe_choice == "peaceful":
        draw_text("The tribe helps you build a boat. You escape!", 20, 100)
    else:
        draw_text("You couldn't escape. Better luck next time!", 20, 100)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Check if any button is clicked

    # Day-based scene rendering
    if day == 1:
        start_day1()
    elif day == 2:
        day2()
    elif day == 3:
        day3()
    
    # Update display and game state
    pygame.display.flip()

pygame.quit()
sys.exit()
