import pygame

class AdjustStats:
    
    @staticmethod
    def addAttackButton(screen):

        add_button = pygame.Rect(20, 30, 20, 20)
        pygame.draw.rect(screen, (0, 0, 0), add_button)
        font = pygame.font.Font(None, 24)  
        text = font.render("+", True, (255, 255, 255))
        text_rect = text.get_rect(center=add_button.center)
        screen.blit(text, text_rect)

        return add_button

    @staticmethod
    def subtractAttackButton(screen):

        subtract_button = pygame.Rect(20, 60, 20, 20)
        pygame.draw.rect(screen, (0, 0, 0), subtract_button)
        font = pygame.font.Font(None, 24)  
        text = font.render("-", True, (255, 255, 255))
        text_rect = text.get_rect(center=subtract_button.center)
        screen.blit(text, text_rect)

        return subtract_button
    
    @staticmethod
    def addHealthButton(screen):

        add_button = pygame.Rect(500, 30, 20, 20)
        pygame.draw.rect(screen, (0, 0, 0), add_button)
        font = pygame.font.Font(None, 24)  
        text = font.render("+", True, (255, 255, 255))
        text_rect = text.get_rect(center=add_button.center)
        screen.blit(text, text_rect)

        return add_button
    
    @staticmethod
    def subtractHealthButton(screen):

        add_button = pygame.Rect(500, 60, 20, 20)
        pygame.draw.rect(screen, (0, 0, 0), add_button)
        font = pygame.font.Font(None, 24)  
        text = font.render("-", True, (255, 255, 255))
        text_rect = text.get_rect(center=add_button.center)
        screen.blit(text, text_rect)

        return add_button
    