import pygame
from sys import exit
 
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Surviving Tinkerer')
clock = pygame.time.Clock()
 
# Load resources
test_font = pygame.font.Font(None, 50)
sky_surface = pygame.image.load('img/dag1img.jpg').convert()
sea_surface = pygame.image.load('img/dag2img.jpg').convert_alpha()
sea_rect = sea_surface.get_rect(midbottom=(80, 300))
text_surface = test_font.render('Surviving Tinkerer', False, 'azure')
 
# Button setup
button_font = pygame.font.Font(None, 40)
button_text = button_font.render('Start', True, 'white')
button_color = (0, 102, 204)  # Dark blue
button_hover_color = (51, 153, 255)  # Lighter blue for hover
button_rect = pygame.Rect(350, 200, 100, 50)  # x, y, width, height
button_active = True  # Whether the button should be displayed
 
# Sea position
sea_x_position = 100
 
# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the button is clicked
            if button_active and button_rect.collidepoint(event.pos):
                button_active = False  # Hide the button after click (start game)
 
    # Draw the sky and moving sea surface
    screen.blit(sky_surface, (0, 0))
    screen.blit(sea_surface, (sea_x_position, 300))
    sea_x_position += 3
    if sea_x_position > 800:
        sea_x_position = -100
    screen.blit(text_surface, (280, 60))
 
    # Draw the button only if active
    if button_active:
        mouse_pos = pygame.mouse.get_pos()
        # Change color on hover
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, (button_rect.x + 15, button_rect.y + 10))
 
    # Update display
    pygame.display.update()
    clock.tick(50)