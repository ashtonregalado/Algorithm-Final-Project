import pygame
from gcd import gcd


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, attack,health, speed = 3, width = 40, height= 40, color= (0, 0, 255), boundary_rect=None, is_character = False):
        
        self.x = x
        self.y = y
        self.attack = attack
        self.health = health
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self.boundary_rect = boundary_rect 
        self.is_character = is_character
        self.font = pygame.font.Font(None, 18)
        self.alive = True 

        try:
            self.image = pygame.image.load("assets/enemy.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.rect = self.image.get_rect(topleft=(x, y))

    def full_health(self):
        return self.health

    def attack_power(self):
        return self.attack
    
    #still has an error where the movement is not responsive when cahracter is at the edge
    def move(self, target_x, target_y, screen_width, screen_height):
        if not self.alive:
            return

        dx = target_x - self.x
        dy = target_y - self.y

        if dx == 0 and dy == 0:
            return

        gcd_value = gcd(abs(dx), abs(dy))
        step_x = dx // gcd_value if gcd_value != 0 else 0
        step_y = dy // gcd_value if gcd_value != 0 else 0

        next_x = self.x + step_x * self.speed
        next_y = self.y + step_y * self.speed

        # Priority 1: respect custom boundary if it exists
        if self.boundary_rect:
            if self.boundary_rect.left <= next_x <= self.boundary_rect.right - self.width:
                self.x = next_x
            if self.boundary_rect.top <= next_y <= self.boundary_rect.bottom - self.height:
                self.y = next_y
        else:
            # fallback: screen boundaries
            if 0 <= next_x <= screen_width - self.width:
                self.x = next_x
            if 0 <= next_y <= screen_height - self.height:
                self.y = next_y

        self.rect.topleft = (self.x, self.y)


    def take_damage(self, damage: int):
        """Reduces health and marks enemy as destroyed if needed."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False  
            


    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect.topleft)

            attack_surface = self.font.render(f"ATK: {self.attack}", True, (0, 0, 0))
            attack_rect = attack_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
            screen.blit(attack_surface, attack_rect)

            health_surface = self.font.render(f"{self.health}", True, (255, 255, 255))
            health_rect = health_surface.get_rect(center=self.rect.center)
            screen.blit(health_surface, health_rect)

        return self.alive

