import pygame
import random

# Initieer pygame
pygame.init()

# Configuratie voor venster en kleur
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Overlevingsspel op het Eiland")

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Spelfuncties
def start_game(dag_limiet=False, max_days=3):
    hp = 100
    day = 1
    door_choice = None
    tribe_choice = None
    running = True
    while hp > 0 and running:
        # Background kleur en tekstweergave
        screen.fill(WHITE)
        render_text(screen, f"Dag {day}, HP: {hp}", (10, 10))

        # Check op daglimiet
        if dag_limiet and day > max_days:
            render_text(screen, f"Gefeliciteerd! Je hebt {max_days} dagen overleefd!", (10, 50))
            pygame.display.flip()
            pygame.time.wait(1000)
            break

        # Begin Spel Acties
        if day == 1:
            render_text(screen, "Dag 1: Zoek naar Hout of Eten (druk 1 of 2)", (10, 100))
            pygame.display.flip()

            choice = get_choice()
            if choice == "1":
                render_text(screen, "Je hebt hout gevonden, +5 HP", (10, 150))
                hp += 5
            elif choice == "2":
                hp = gather_food(hp)
            else:
                continue

            pygame.display.flip()
            pygame.time.wait(1000)

            # Nacht op dag 1
            if choice == "1":
                render_text(screen, "Je blijft warm bij het vuur, maar verliest -5 HP door honger.", (10, 200))
                hp -= 5
            else:
                render_text(screen, "Je verliest -10 HP door koude nacht zonder vuur.", (10, 200))
                hp -= 10
            pygame.display.flip()
            pygame.time.wait(1000)

        # Dag 2 Acties
        elif day == 2:
            render_text(screen, "Dag 2: Verken het eiland (Oost of West, druk 1 of 2)", (10, 100))
            pygame.display.flip()
            
            choice_day2 = get_choice()
            if choice_day2 == "1":
                water_choice = get_subchoice("Tempel gevonden: pak object (1) of verken verder (2)")
                if water_choice == "1":
                    hp = computer_choice(hp)
                    hp -= 15
                elif water_choice == "2":
                    door_choice = get_subchoice("Twee deuren gevonden: links (1) of rechts (2)")
                    if door_choice == "1":
                        render_text(screen, "Hulpmaterialen gevonden om signaal te maken.", (10, 200))
                    elif door_choice == "2":
                        render_text(screen, "Slangen! -100 HP", (10, 200))
                        hp -= 100
            elif choice_day2 == "2":
                tribe_choice = get_subchoice("Tribe ontmoet: communiceren (1) of vechten (2)")
                if tribe_choice == "1":
                    render_text(screen, "Tribe helpt je, +10 HP", (10, 200))
                    hp += 10
                elif tribe_choice == "2":
                    render_text(screen, "Tribe doodt je. -100 HP", (10, 200))
                    hp -= 100

        # Dag 3 Acties
        elif day == 3:
            render_text(screen, "Dag 3: Laatste kans voor ontsnapping!", (10, 100))
            pygame.display.flip()
            pygame.time.wait(1000)

            if door_choice == "1":
                render_text(screen, "Hulpsignaal werkt, je wordt gered!", (10, 150))
            elif tribe_choice == "1":
                render_text(screen, "Tribe helpt je met boot, je ontsnapt!", (10, 150))
            else:
                render_text(screen, "Geheime einde ontgrendeld", (10, 150))
            pygame.display.flip()
            pygame.time.wait(1000)
            break

        day += 1

        if hp <= 0:
            render_text(screen, "Je HP is op. Je hebt het niet overleefd.", (10, 100))
            pygame.display.flip()
            pygame.time.wait(1000)
            break

def get_choice():
    """Kies optie met 1 of 2-toets."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "1"
                elif event.key == pygame.K_2:
                    return "2"

def get_subchoice(prompt):
    """Prompt speler voor keuze in submenu."""
    screen.fill(WHITE)
    render_text(screen, prompt, (10, 100))
    pygame.display.flip()
    return get_choice()

def computer_choice(hp):
    outcomes = [
        {"message": "Object wijst naar geheim koninkrijk. Koning!", "hp_change": 0},
        {"message": "Object is een bom. -100 HP", "hp_change": -100}
    ]
    outcome = random.choice(outcomes)
    render_text(screen, outcome["message"], (10, 150))
    hp += outcome["hp_change"]
    pygame.display.flip()
    pygame.time.wait(1000)
    return hp

def gather_food(hp):
    sub_choice = get_subchoice("Eten zoeken: Bessen (1) of Jagen (2)?")
    if sub_choice == "1":
        render_text(screen, "Giftige bessen -10 HP", (10, 150))
        hp -= 10
    elif sub_choice == "2":
        sub_choice2 = get_subchoice("Maak wapen (1) of jaag met handen (2)?")
        if sub_choice2 == "1":
            render_text(screen, "Wapen breekt bij beer, -100 HP", (10, 200))
            hp -= 100
        elif sub_choice2 == "2":
            render_text(screen, "Je vangt vis, +10 HP", (10, 200))
            hp += 10
    pygame.display.flip()
    pygame.time.wait(1000)
    return hp

def render_text(screen, text, position):
    """Tekstweergave op scherm"""
    label = FONT.render(text, True, BLACK)
    screen.blit(label, position)

# Start het spel
start_game(dag_limiet=True, max_days=3)
pygame.quit()
