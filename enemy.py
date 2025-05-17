import pygame
import math
import random
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, attack, health, width=40, height=90, color=(255, 0, 0), boundary_rect=None, is_general=False, is_final_boss=False):
        # super().__init__()
        self.x = x
        self.y = y
        self.attack = attack
        self.health = health
        self.width = width
        self.height = height
        self.color = color
        self.font = pygame.font.Font(None, 18)
        self.alive = True
        self.last_fire_time = pygame.time.get_ticks()
        self.fire_delay = random.randint(500, 1500)
        self.is_general = is_general
        self.is_final_boss = is_final_boss

        self.direction = -1
        self.speed = 2

        while True:
            self.dx = random.choice([-1, 1]) * self.speed
            self.dy = random.choice([-1, 1]) * self.speed
            if self.dx != 0 and self.dy != 0:
                break

        self.boundary = boundary_rect
        # Load enemy sprite (fallback to rectangle if not using images)
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
    
    @staticmethod
    def random_direction(speed):
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle) * speed, math.sin(angle) * speed

    def move(self):
        if not self.alive:
            return

        # Move using float precision
        self.x += self.dx
        self.y += self.dy

        # Update rect for display (use int conversion for rendering)
        self.rect.topleft = (int(self.x), int(self.y))

        if self.boundary:
            bounced = False

            # Create a temp rect from float x/y
            temp_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

            if not self.boundary.contains(temp_rect):
                temp_rect.clamp_ip(self.boundary)
                self.x, self.y = temp_rect.topleft
                bounced = True

            # Left/right
            if temp_rect.left <= self.boundary.left:
                self.x = self.boundary.left
                bounced = True
            elif temp_rect.right >= self.boundary.right:
                self.x = self.boundary.right - self.width
                bounced = True

            # Top/bottom
            if temp_rect.top <= self.boundary.top:
                self.y = self.boundary.top
                bounced = True
            elif temp_rect.bottom >= self.boundary.bottom:
                self.y = self.boundary.bottom - self.height
                bounced = True

            if bounced:
                self.dx, self.dy = self.random_direction(self.speed)

        self.rect.topleft = (int(self.x), int(self.y))


    def take_damage(self, damage: int):
        """Reduces health and marks enemy as destroyed if needed."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False  
            

    def draw(self, screen):
        """Draws the enemy, displaying attack above and health in the middle."""
        if self.alive:
            screen.blit(self.image, self.rect.topleft)

            attack_surface = self.font.render(f"ATK: {self.attack}", True, (0, 0, 0))
            attack_rect = attack_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
            screen.blit(attack_surface, attack_rect)


            health_surface = self.font.render(f"{self.health}", True, (255, 255, 255))
            health_rect = health_surface.get_rect(center=self.rect.center)
            screen.blit(health_surface, health_rect)

        return self.alive

