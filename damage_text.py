import pygame

class DamageText:

    def __init__(self, x, y, damage, color=(255, 0, 0), duration=30):
        self.x = x
        self.y = y
        self.damage = damage
        self.font =  pygame.font.Font(None, 30)
        self.color = color
        self.duration = duration
    
    def update(self):
        
        self.y -= 1
        self.duration -= 1

    def draw(self, screen):
        if self.duration > 0:
            text = self.font.render(f'-{self.damage}', True, self.color)
            screen.blit(text, (self.x, self.y))