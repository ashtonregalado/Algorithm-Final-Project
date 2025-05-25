import pygame

def gameOver(screen, WIDTH, HEIGHT, winner):
    font_title = pygame.font.Font("assets/PixeloidSans.ttf", 72)
    font_button = pygame.font.Font("assets/PixeloidMono.ttf", 28)

    title_text = font_title.render("Game Over", True, (255, 255, 255))
    character_wins_text = font_button.render("You Win", True, (255, 255, 255))
    enemy_wins_text = font_button.render("You Lose", True, (255, 255, 255))
    retry_text = font_button.render("Press R to Retry or Q to Quit", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r:
                    return  # Exit gameOver screen to restart game

        screen.fill((0, 0, 0))  # Clear screen with black background


        # Draw texts
        # Draw "Game Over" title
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw winner message
        winner_text = character_wins_text if winner == "character" else enemy_wins_text
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3 + 50))

        # Draw retry instruction
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
