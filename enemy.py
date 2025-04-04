import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y,attack, health, width=40, height=90, color=(255, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.attack = attack
        self.health = health
        self.width = width
        self.height = height
        self.color = color
        self.font = pygame.font.Font(None, 18)
        self.alive = True  # Tracks if enemy is still active

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

