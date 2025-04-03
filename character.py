import pygame
from enemy import Enemy
from gcd import gcd


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, attack, speed = 3, width = 40, height= 40, color= (0, 0, 255)):
        
        self.x = x
        self.y = y
        self.attack = attack
        self.speed = speed
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
    
    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y

        if dx == 0 and dy == 0:
            return
        
        # Use Euclid's Algorithm (GCD) to find the greatest common divisor for smooth movement
        gcd_value = gcd(abs(dx), abs(dy))  # Calculate GCD for normalized movement steps
        step_x = dx // gcd_value if gcd_value != 0 else 0
        step_y = dy // gcd_value if gcd_value != 0 else 0

        # Move the character by the computed steps
        self.x += step_x * self.speed
        self.y += step_y * self.speed

        # Update the rect position after moving
        self.rect.topleft = (self.x, self.y)


    def draw(self, screen):

        
        screen.blit(self.image, self.rect.topleft)

        text_surface = self.font.render(str(self.attack), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
