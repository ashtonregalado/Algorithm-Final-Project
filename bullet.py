import pygame

class Bullet:

    def __init__(self, x, y, direction = 1,speed =10, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.color = color
        self.width = 20
        self.height = 20
        self.active = True

    def update(self):
        self.x += self.speed * self.direction

        if self.x > 800:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self. width, self.height))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)