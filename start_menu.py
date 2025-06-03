import pygame
from menu_background import drawBackground

def startMenu(screen, backgrounds, WIDTH, HEIGHT):
    font_title = pygame.font.Font("assets/PixeloidSans.ttf", 72)
    font_button = pygame.font.Font("assets/PixeloidMono.ttf", 22)

    title_text = font_title.render("Euclid's Algorithm", True, (255, 255, 255))
    start_text = font_button.render("Start Game", True, (0, 0, 0))

    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    while True:
        drawBackground(screen, backgrounds)

        # Draw title
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw start button
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        screen.blit(start_text, (button_x + (button_width - start_text.get_width()) // 2,
                                 button_y + (button_height - start_text.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return # Exit menu and start the game

        pygame.display.flip()