import pygame

class Bullet:
    def __init__(self, x, y, direction=1, speed=5, color=(0, 0, 0), owner=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.color = color
        self.owner = owner
        self.active = True

        # Default bullet size
        width = 10
        height = 10

        # Customize if bullet is from general or boss
        if self.owner:
            if hasattr(self.owner, "is_general") and self.owner.is_general:
                self.color = (255, 0, 0)
                self.speed = 10
                width = 15
                height = 15
            elif hasattr(self.owner, "is_final_boss") and self.owner.is_final_boss:
                self.color = (128, 0, 128)
                self.speed = 20
                width = 25
                height = 25
            elif hasattr(self.owner, "is_character"):
                self.color = (100, 100, 100)
                self.speed = 5
                width = 15
                height = 15

        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x += self.speed * self.direction
        self.x = self.rect.x  # keep x in sync
        if self.rect.right < 0 or self.rect.left > 800:
            self.active = False
        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
