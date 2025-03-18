import pygame
from enemy import Enemy


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, attack, width = 40, height= 40, color= (0, 0, 255)):
        
        self.x = x
        self.y = y
        self.attack = attack
        self.width = width
        self.height = height
        self.color = color
        self.font = pygame.font.Font(None, 18)

        try:
            self.image = pygame.image.load("assets/enemy.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.rect = self.image.get_rect(topleft=(x, y))


    def attack_power(self):
        return self.attack


    def draw(self, screen):

        
        screen.blit(self.image, self.rect.topleft)

        text_surface = self.font.render(str(self.attack), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
